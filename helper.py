from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. Total messages
    num_messages = df.shape[0]

    # 2. Total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. Media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. Links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    # Exclude group notifications
    df = df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percent_df.columns = ['Name', 'Percent']
    return x, percent_df


def create_wordcloud(selected_user, df):

    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
        

    # Exclude group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Remove group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user,df):


    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
        

    # Exclude group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    timeline = df.groupby(['year' , 'month_num']).count()['message'].reset_index()


    time =[ ]

    for i in range(timeline.shape[0]):
        time.append(str(timeline['month_num'][i]) + '-' + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap


# ============================================================
# NEW FEATURE: Sentiment Analysis (VADER)
# ============================================================

def sentiment_analysis(selected_user, df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    analyzer = SentimentIntensityAnalyzer()

    sentiments = []
    for message in df['message']:
        score = analyzer.polarity_scores(str(message))
        compound = score['compound']
        if compound >= 0.05:
            sentiments.append('Positive')
        elif compound <= -0.05:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')

    sentiment_df = df.copy()
    sentiment_df['sentiment'] = sentiments

    # Distribution counts
    distribution = pd.DataFrame(Counter(sentiments).items(), columns=['Sentiment', 'Count'])

    return sentiment_df, distribution


def sentiment_over_time(selected_user, df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    analyzer = SentimentIntensityAnalyzer()

    df = df.copy()
    df['compound'] = df['message'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])

    # Group by date and get mean sentiment
    sentiment_time = df.groupby('only_date')['compound'].mean().reset_index()
    sentiment_time.columns = ['Date', 'Avg Sentiment']

    return sentiment_time


# ============================================================
# NEW FEATURE: Topic Modeling (LDA)
# ============================================================

def topic_modeling(selected_user, df, n_topics=5):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    messages = temp['message'].tolist()

    # Need at least some messages
    if len(messages) < 10:
        return None, None

    # Load stop words
    try:
        f = open('stop_hinglish.txt', 'r')
        custom_stops = f.read().split()
        f.close()
    except:
        custom_stops = []

    # Vectorize
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english',
                                  max_features=1000)
    try:
        doc_term_matrix = vectorizer.fit_transform(messages)
    except:
        return None, None

    # Fit LDA
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42,
                                     max_iter=10)
    lda.fit(doc_term_matrix)

    # Extract top keywords per topic
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    for idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
        topics[f'Topic {idx+1}'] = top_words

    topics_df = pd.DataFrame(topics)

    # Topic distribution
    topic_dist = lda.transform(doc_term_matrix)
    avg_dist = topic_dist.mean(axis=0)
    dist_df = pd.DataFrame({
        'Topic': [f'Topic {i+1}' for i in range(n_topics)],
        'Weight': avg_dist
    })

    return topics_df, dist_df


# ============================================================
# SUMMARY UPDATE: Smart Chat Summary (Multilingual + Topic-Aware)
# ============================================================

# Hindi/Bengali common stopwords (supplement to stop_hinglish.txt)
_EXTRA_STOPWORDS = {
    'hai', 'hain', 'ho', 'tha', 'thi', 'the', 'ke', 'ka', 'ki', 'ko', 'se',
    'me', 'mein', 'par', 'pe', 'ne', 'bhi', 'aur', 'ya', 'jo', 'ye', 'wo',
    'kya', 'kab', 'kaise', 'kahan', 'kyun', 'nahi', 'nai', 'na', 'mat',
    'toh', 'to', 'hi', 'bhai', 'yaar', 'arre', 'haa', 'hmm', 'ok', 'okay',
    'accha', 'theek', 'bas', 'abhi', 'woh', 'yeh', 'iska', 'uska', 'apna',
    'kuch', 'sab', 'bahut', 'zyada', 'kam', 'wala', 'wali', 'wale',
    # Bengali common words
    'ami', 'tumi', 'apni', 'she', 'shey', 'eta', 'ota', 'ki', 'keno',
    'kothay', 'kokhon', 'ache', 'nei', 'hobe', 'korbo', 'koro', 'bolo',
    'jani', 'ar', 'o', 'r', 'ta', 'te', 'er', 'ke', 'theke',
    # Common chat noise
    'deleted', 'message', 'media', 'omitted', 'http', 'https', 'www',
}


def _load_all_stopwords():
    """Load Hinglish stopwords file + extra multilingual stops."""
    stops = set(_EXTRA_STOPWORDS)
    try:
        with open('stop_hinglish.txt', 'r') as f:
            stops.update(f.read().split())
    except:
        pass
    return stops


def chat_summary(selected_user, df, sentence_count=5):
    """SUMMARY UPDATE: Generates a structured, topic-aware, multilingual summary."""
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out noise
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    messages = temp['message'].tolist()
    total_msgs = df.shape[0]

    if len(messages) < 5:
        return "Not enough text data to generate a summary."

    # --- 1. Sentiment overview ---
    analyzer = SentimentIntensityAnalyzer()
    pos, neg, neu = 0, 0, 0
    for msg in messages:
        score = analyzer.polarity_scores(str(msg))['compound']
        if score >= 0.05:
            pos += 1
        elif score <= -0.05:
            neg += 1
        else:
            neu += 1

    total_scored = pos + neg + neu
    if total_scored > 0:
        dominant = max([('positive', pos), ('negative', neg), ('neutral', neu)], key=lambda x: x[1])
        sentiment_pct = round((dominant[1] / total_scored) * 100, 1)
        sentiment_line = f"The overall tone is {dominant[0]} ({sentiment_pct}% of messages)."
    else:
        sentiment_line = "The overall tone could not be determined."

    # --- 2. Topic keywords (lightweight — no full LDA, just word freq) ---
    stop_words = _load_all_stopwords()

    word_freq = Counter()
    for msg in messages:
        for word in str(msg).lower().split():
            # Clean punctuation
            clean = ''.join(c for c in word if c.isalnum())
            if clean and len(clean) > 2 and clean not in stop_words:
                word_freq[clean] += 1

    top_keywords = [word for word, _ in word_freq.most_common(8)]

    if top_keywords:
        keyword_str = ', '.join(top_keywords[:5])
        topic_line = f"Key discussion topics include: {keyword_str}."
    else:
        topic_line = "No dominant discussion topics could be identified."

    # --- 3. Activity pattern ---
    if 'hour' in df.columns:
        peak_hour = df['hour'].value_counts().idxmax()
        if peak_hour < 6:
            time_desc = "late night"
        elif peak_hour < 12:
            time_desc = "morning"
        elif peak_hour < 17:
            time_desc = "afternoon"
        elif peak_hour < 21:
            time_desc = "evening"
        else:
            time_desc = "night"
        activity_line = f"Most conversations happen during the {time_desc} (peak around {peak_hour}:00)."
    else:
        activity_line = ""

    # --- 4. User context ---
    num_users = df[df['user'] != 'group_notification']['user'].nunique()
    media_count = df[df['message'] == '<Media omitted>\n'].shape[0]

    if selected_user == 'Overall':
        user_line = f"The chat involves {num_users} participants with a total of {total_msgs} messages."
    else:
        user_line = f"{selected_user} sent {total_msgs} messages in this chat."

    media_line = ""
    if media_count > 0:
        media_line = f" {media_count} media files were shared."

    # --- 5. Recurring words highlight ---
    if len(top_keywords) >= 3:
        recurring_line = f"Recurring words like {', '.join(top_keywords[:3])} suggest the conversation frequently revolves around these subjects."
    else:
        recurring_line = ""

    # --- Assemble summary ---
    summary_parts = [user_line + media_line, topic_line, sentiment_line]
    if activity_line:
        summary_parts.append(activity_line)
    if recurring_line:
        summary_parts.append(recurring_line)

    return ' '.join(summary_parts)


# ============================================================
# NEW FEATURE: Response Time Analysis
# ============================================================

def response_time_analysis(selected_user, df):

    # Filter out group notifications
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp.sort_values('date').reset_index(drop=True)

    response_times = []

    for i in range(1, len(temp)):
        # Only count when sender changes (actual response)
        if temp['user'][i] != temp['user'][i-1]:
            time_diff = (temp['date'][i] - temp['date'][i-1]).total_seconds() / 60  # in minutes
            # Only count reasonable response times (< 24 hours)
            if 0 < time_diff < 1440:
                response_times.append({
                    'user': temp['user'][i],
                    'response_time_min': time_diff
                })

    if not response_times:
        return pd.DataFrame(columns=['user', 'Avg Response Time (min)'])

    rt_df = pd.DataFrame(response_times)

    # Average response time per user
    avg_rt = rt_df.groupby('user')['response_time_min'].mean().reset_index()
    avg_rt.columns = ['User', 'Avg Response Time (min)']
    avg_rt['Avg Response Time (min)'] = round(avg_rt['Avg Response Time (min)'], 2)
    avg_rt = avg_rt.sort_values('Avg Response Time (min)')

    if selected_user != 'Overall':
        avg_rt = avg_rt[avg_rt['User'] == selected_user]

    return avg_rt


# ============================================================
# NEW FEATURE: Smart Chat Insights Engine
# ============================================================

def generate_insights(df, selected_user):

    insights = []

    # Filter for selected user
    if selected_user != 'Overall':
        user_df = df[df['user'] == selected_user]
    else:
        user_df = df[df['user'] != 'group_notification']

    # --- Insight 1: Most active user ---
    if selected_user == 'Overall':
        top_user = df[df['user'] != 'group_notification']['user'].value_counts().idxmax()
        top_count = df[df['user'] != 'group_notification']['user'].value_counts().max()
        insights.append(f"🏆 {top_user} is the most active user with {top_count} messages.")

    # --- Insight 2: Peak activity hour ---
    peak_hour = user_df['hour'].value_counts().idxmax()
    if peak_hour < 6:
        time_label = "late night 🌙"
    elif peak_hour < 12:
        time_label = "morning ☀️"
    elif peak_hour < 17:
        time_label = "afternoon 🌤️"
    elif peak_hour < 21:
        time_label = "evening 🌆"
    else:
        time_label = "night 🌙"

    if selected_user != 'Overall':
        insights.append(f"⏰ {selected_user} is most active around {peak_hour}:00 ({time_label}).")
    else:
        insights.append(f"⏰ The group is most active around {peak_hour}:00 ({time_label}).")

    # --- Insight 3: Busiest day of the week ---
    if 'day_name' in user_df.columns:
        busiest_day = user_df['day_name'].value_counts().idxmax()
        day_count = user_df['day_name'].value_counts().max()
        insights.append(f"📅 Most conversations happen on {busiest_day} ({day_count} messages).")

    # --- Insight 4: Average message length ---
    avg_words = user_df['message'].apply(lambda x: len(str(x).split())).mean()
    if avg_words < 3:
        style = "short and quick"
    elif avg_words < 8:
        style = "moderate-length"
    else:
        style = "detailed and long"
    insights.append(f"💬 Messages are typically {style} (avg {avg_words:.1f} words per message).")

    # --- Insight 5: Response time (Overall only) ---
    if selected_user == 'Overall':
        try:
            avg_rt = response_time_analysis('Overall', df)
            if not avg_rt.empty:
                fastest = avg_rt.iloc[0]
                insights.append(
                    f"⚡ {fastest['User']} responds the fastest with an average of {fastest['Avg Response Time (min)']:.1f} minutes."
                )
        except:
            pass

    # --- Insight 6: Media sharing ---
    media_count = user_df[user_df['message'] == '<Media omitted>\n'].shape[0]
    total = user_df.shape[0]
    if total > 0:
        media_pct = (media_count / total) * 100
        insights.append(f"📷 {media_pct:.1f}% of messages are media (images/videos/documents).")

    return insights