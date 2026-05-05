import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# UI UPDATE: Page config
# ============================================================

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

# UI POLISH: Red/Black theme with refined soft glow
st.markdown("""
<style>
    /* Global */
    .block-container { padding-top: 1.5rem; }
    [data-testid="stAppViewContainer"] {
        background: #0f1117;
    }
    [data-testid="stSidebar"] {
        background: #1a1a2e;
    }

    /* Cards — soft red glow */
    .card {
        background: #1a1d24;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(255, 75, 75, 0.35);
        box-shadow:
            0px 4px 12px rgba(255, 75, 75, 0.12),
            0px 0px 20px rgba(255, 75, 75, 0.06);
        margin-bottom: 18px;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1d24 0%, #251520 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 75, 75, 0.35);
        text-align: center;
        box-shadow:
            0px 4px 12px rgba(255, 75, 75, 0.12),
            0px 0px 18px rgba(255, 75, 75, 0.06);
    }
    .metric-card .label {
        color: #ff6b6b;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }

    /* Insight boxes — clean with subtle glow */
    .insight-box {
        padding: 12px 16px;
        border-left: 3px solid #ff4b4b;
        background: #11131a;
        border-radius: 0 6px 6px 0;
        margin-bottom: 10px;
        color: #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0px 2px 8px rgba(255, 75, 75, 0.06);
    }

    /* Summary box */
    .summary-box {
        padding: 22px;
        border-radius: 12px;
        background: #141a14;
        border: 1px solid rgba(75, 200, 75, 0.25);
        color: #c8e6c8;
        line-height: 1.8;
        font-size: 0.95rem;
        box-shadow: 0px 4px 12px rgba(75, 200, 75, 0.08);
    }

    /* Section divider */
    .section-divider {
        margin: 35px 0;
        border: none;
        border-top: 1px solid rgba(255, 75, 75, 0.15);
    }

    /* Section header */
    .section-header {
        color: #ff6b6b;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .sub-header {
        color: #cccccc;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# UI UPDATE: Sidebar — branding + instructions
# ============================================================

st.sidebar.markdown("## 💬 WhatsApp Chat Analyzer")
st.sidebar.markdown("*AI-powered chat analytics*")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**How to use:**
1. 📤 Upload a WhatsApp chat export (.txt)
2. 👤 Select a user or 'Overall'
3. 📊 Analysis runs automatically!
""")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader('Upload WhatsApp Chat (.txt)')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # FIXED: Safety check for empty dataframe
    if df.empty:
        st.error("⚠️ Could not parse chat data. Please check the file format.")
        st.stop()

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis for:', user_list)

    # FIXED: Auto-render — removed button dependency, analysis runs on upload + user select

    # ================================================================
    # SECTION 1: Top Statistics
    # ================================================================

    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Top Statistics</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">📩 TOTAL MESSAGES</div>
            <div class="value">{num_messages}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">📝 TOTAL WORDS</div>
            <div class="value">{words}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🖼️ MEDIA SHARED</div>
            <div class="value">{num_media_messages}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">🔗 LINKS SHARED</div>
            <div class="value">{num_links}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 2: Timelines
    # ================================================================

    st.markdown('<div class="section-header">📈 Timelines</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Monthly Timeline</div>', unsafe_allow_html=True)
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(timeline['time'], timeline['message'], color='#27ae60', linewidth=2, marker='o', markersize=4)
    ax.set_xlabel('Month-Year')
    ax.set_ylabel('Message Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Daily Timeline</div>', unsafe_allow_html=True)
    daily_tl = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily_tl['only_date'], daily_tl['message'], color='#e67e22', linewidth=1.5)
    ax.set_xlabel('Date')
    ax.set_ylabel('Message Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 3: Activity Analysis
    # ================================================================

    st.markdown('<div class="section-header">🗓️ Activity Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Most Busy Day</div>', unsafe_allow_html=True)
        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(busy_day.index, busy_day.values, color='#3498db')
        ax.set_ylabel('Message Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Most Busy Month</div>', unsafe_allow_html=True)
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(busy_month.index, busy_month.values, color='#e67e22')
        ax.set_ylabel('Message Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Weekly Activity Heatmap</div>', unsafe_allow_html=True)
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.heatmap(user_heatmap, ax=ax, cmap='YlOrRd', linewidths=0.5)
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Day')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 4: User Analysis (Overall only)
    # ================================================================

    if selected_user == 'Overall':
        st.markdown('<div class="section-header">👥 User Analysis</div>', unsafe_allow_html=True)

        x, new_df = helper.most_busy_users(df)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sub-header">Top 10 Most Active Users</div>', unsafe_allow_html=True)
            top_users = x.head(10).sort_values()
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(top_users.index, top_users.values, color='#e74c3c')
            ax.set_xlabel('Message Count')
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                        f'{int(width)}', va='center', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sub-header">User Activity Breakdown</div>', unsafe_allow_html=True)
            st.dataframe(new_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 5: Text Analysis
    # ================================================================

    st.markdown('<div class="section-header">🔤 Text Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">WordCloud</div>', unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Top 20 Most Common Words</div>', unsafe_allow_html=True)
        most_common_df = helper.most_common_words(selected_user, df)
        most_common_sorted = most_common_df.sort_values('count')
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(most_common_sorted['word'], most_common_sorted['count'], color='#ff4b4b')
        ax.set_xlabel('Frequency')
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', va='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Emoji Analysis
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">😀 Emoji Analysis</div>', unsafe_allow_html=True)
    emoji_df = helper.emoji_helper(selected_user, df)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df, use_container_width=True)

    with col2:
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        fig, ax = plt.subplots()
        if not emoji_df.empty:
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
        st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 6: NLP Analysis
    # ================================================================

    st.markdown('<div class="section-header">🧠 NLP Analysis</div>', unsafe_allow_html=True)

    # --- Sentiment ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sentiment Analysis</div>', unsafe_allow_html=True)

    sentiment_df, sentiment_dist = helper.sentiment_analysis(selected_user, df)

    col1, col2 = st.columns(2)

    with col1:
        if not sentiment_dist.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}
            bar_colors = [colors.get(s, '#95a5a6') for s in sentiment_dist['Sentiment']]
            bars = ax.bar(sentiment_dist['Sentiment'], sentiment_dist['Count'], color=bar_colors)
            ax.set_ylabel('Count')
            ax.set_title('Sentiment Distribution')
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                        f'{int(height)}', ha='center', fontsize=10)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("No sentiment data available.")

    with col2:
        sentiment_time = helper.sentiment_over_time(selected_user, df)
        if not sentiment_time.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(sentiment_time['Date'], sentiment_time['Avg Sentiment'], color='#8e44ad', linewidth=2)
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
            ax.set_ylabel('Avg Sentiment Score')
            ax.set_xlabel('Date')
            ax.set_title('Sentiment Over Time')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("No sentiment timeline data available.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Topic Modeling ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">📑 Topic Modeling</div>', unsafe_allow_html=True)

    if st.button("🔍 Extract Topics"):
        with st.spinner("Running LDA Topic Modeling..."):
            topics_df, dist_df = helper.topic_modeling(selected_user, df)

        if topics_df is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(topics_df, use_container_width=True)
            with col2:
                fig, ax = plt.subplots(figsize=(8, 5))
                bars = ax.bar(dist_df['Topic'], dist_df['Weight'], color='#00838f')
                ax.set_ylabel('Avg Weight')
                ax.set_title('Topic Weight Distribution')
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, height,
                            f'{height:.3f}', ha='center', va='bottom', fontsize=9)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
        else:
            st.warning("Not enough messages to extract topics. Need at least 10 messages.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Response Time ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">⏱️ Response Time Analysis</div>', unsafe_allow_html=True)

    avg_rt = helper.response_time_analysis(selected_user, df)

    if not avg_rt.empty:
        col1, col2 = st.columns(2)

        with col1:
            rt_sorted = avg_rt.head(15).sort_values('Avg Response Time (min)')
            fig, ax = plt.subplots(figsize=(10, max(4, len(rt_sorted) * 0.5)))
            bars = ax.barh(rt_sorted['User'], rt_sorted['Avg Response Time (min)'], color='#ff7043')
            ax.set_xlabel('Minutes')
            ax.set_title('Average Response Time')
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}', va='center', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

        with col2:
            st.dataframe(avg_rt, use_container_width=True)
    else:
        st.info("Not enough data to calculate response times.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 7: Smart Insights
    # ================================================================

    st.markdown('<div class="section-header">🧠 Smart Insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    insights = helper.generate_insights(df, selected_user)

    if insights:
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    else:
        st.info("Could not generate insights. Check if there's enough data.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ================================================================
    # SECTION 8: Chat Summary
    # ================================================================

    st.markdown('<div class="section-header">📋 Chat Summary</div>', unsafe_allow_html=True)

    # FIXED: Summary button works outside the old button block now
    if st.button("✨ Generate Smart Summary"):
        with st.spinner("Analyzing chat patterns, topics, and sentiment..."):
            summary = helper.chat_summary(selected_user, df)

        # FIXED: Fallback safety for empty summary
        if summary and len(summary.strip()) > 0:
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Summary could not be generated. Please check if there's enough text data in the chat.")
    else:
        st.markdown("*Click the button above to generate an AI-powered summary with topic analysis and sentiment overview.*")

else:
    # FIXED: Show welcome screen when no file uploaded
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="color: #ff4b4b;">💬 WhatsApp Chat Analyzer</h1>
        <p style="color: #888; font-size: 1.2rem;">Upload a WhatsApp chat export to get started</p>
        <p style="color: #666; font-size: 0.9rem; margin-top: 20px;">
            📤 Use the sidebar to upload your .txt file
        </p>
    </div>
    """, unsafe_allow_html=True)
