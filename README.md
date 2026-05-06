# 💬 WhatsApp Chat Analyzer

A complete end-to-end WhatsApp Chat Analysis web application built using **Python**, **Streamlit**, **Data Analysis**, and **Natural Language Processing (NLP)** techniques.

This project allows users to upload exported WhatsApp chats and get detailed insights such as:

* Message statistics
* User activity trends
* Sentiment analysis
* Topic modeling
* Response time analysis
* Smart behavioral insights
* Chat summarization
* Privacy protection through phone masking

The application is fully deployed online using Streamlit Community Cloud.

---

# 🚀 Live Demo

🔗 https://whatsapp-chat-analyzer-debayudh.streamlit.app/


# 📌 Features

## 📊 Basic Chat Analytics

* Total messages
* Total words
* Media shared count
* Links shared count
* Most active users

---

## 📈 Activity Analysis

* Monthly timeline
* Daily timeline
* Weekly activity analysis
* Monthly activity analysis
* Heatmaps for user activity

---

## ☁️ Word Analysis

* WordCloud generation
* Most common words
* Emoji analysis

---

## 🧠 NLP & AI Features

* Sentiment Analysis
* Topic Modeling
* Smart Insights Generator
* Response Time Analysis
* Chat Summarization
* Multilingual text handling

---

## 🔐 Security & Privacy

* Phone number masking
* User privacy protection
* Safe preprocessing before analysis

---

## 🎨 UI Features

* Sidebar navigation
* Responsive dashboard
* Card-style UI
* Hover button effects
* Loading spinner/GIF
* Clean dark-themed design

---

# 🛠️ Tech Stack

| Technology                | Purpose                              |
| ------------------------- | ------------------------------------ |
| Python                    | Core programming language            |
| Streamlit                 | Web app framework                    |
| Pandas                    | Data manipulation and analysis       |
| Matplotlib                | Data visualization                   |
| Seaborn                   | Heatmaps and advanced visualizations |
| WordCloud                 | Word cloud generation                |
| Scikit-learn              | Machine learning & topic modeling    |
| TextBlob / VaderSentiment | Sentiment analysis                   |
| NLTK                      | NLP preprocessing                    |
| Regex (re)                | Chat parsing & preprocessing         |
| Emoji Library             | Emoji extraction & analysis          |
| URLExtract                | URL detection                        |

Humanity really did decide that every problem should involve 14 Python libraries and one emotional support regex.

---

# 📂 Project Structure

```bash
📦 whatsapp-chat-analyzer
 ┣ 📜 app.py
 ┣ 📜 helper.py
 ┣ 📜 preprocessor.py
 ┣ 📜 stop_hinglish.txt
 ┣ 📜 requirements.txt
 ┣ 📜 README.md
```

---

# 📄 File Explanation

## 1. app.py

Main Streamlit application file.

Responsible for:

* UI rendering
* File upload
* Calling helper functions
* Displaying charts
* Handling user interactions

---

## 2. helper.py

Contains all analysis-related functions.

Includes:

* Statistics generation
* WordCloud logic
* Sentiment analysis
* Topic modeling
* Insights generation
* Response time analysis
* Summary generation

---

## 3. preprocessor.py

Responsible for:

* Parsing WhatsApp exported chats
* Extracting users and messages
* Date/time conversion
* Creating structured DataFrame
* Phone number masking

---

## 4. stop_hinglish.txt

Custom stopword file.

Contains:

* English stopwords
* Hinglish stopwords
* Common informal words

Used to improve:

* Word analysis
* Topic extraction
* Summarization

---

# ⚙️ How It Works

## Step 1: Export WhatsApp Chat

From WhatsApp:

1. Open any chat
2. Tap ⋮ (three dots)
3. Click More
4. Click Export Chat
5. Choose "Without Media"

WhatsApp exports the chat as a ZIP file containing a `.txt` file.

---

## Step 2: Upload File

The user uploads:

* `.txt` file
  OR
* `.zip` file directly

The application automatically:

* Reads the file
* Extracts text
* Handles encoding issues
* Preprocesses the chat

---

## Step 3: Analysis

The app performs:

* Statistical analysis
* NLP processing
* Sentiment analysis
* Topic extraction
* Visualization generation

---

## Step 4: Dashboard Display

Interactive charts and insights are shown on the Streamlit dashboard.

---

# 🧠 Advanced Features Explained

## 📌 Sentiment Analysis

Used to identify:

* Positive messages
* Negative messages
* Neutral messages

Libraries used:

* VaderSentiment
* TextBlob

Why used?
Because raw chat data is meaningless unless emotional patterns are extracted. Humans apparently enjoy quantifying feelings now.

---

## 📌 Topic Modeling

Used to identify common discussion themes.

Example topics:

* College
* Exams
* Travel
* Gaming
* Work

Technique used:

* LDA (Latent Dirichlet Allocation)

Library used:

* Scikit-learn

---

## 📌 Response Time Analysis

Measures:

* Average reply time
* User responsiveness
* Communication behavior

Useful for:

* Group activity analysis
* Behavioral insights

---

## 📌 Smart Insights

Automatically generates observations such as:

* Most active user
* Most active time
* Most common discussion behavior
* Fastest responder

---

## 📌 Chat Summarization

Creates a concise summary of long conversations.

Supports:

* English
* Hindi/Hinglish
* Bengali/Roman Bengali

---

# 🔐 Privacy & Security

The application includes:

* Phone number masking
* Safe preprocessing
* No permanent data storage
* Local temporary analysis only

Example:

```bash
+91 9876543210
↓
+91 98765XXXXX
```

Because exposing people's phone numbers online is generally considered a bad social strategy.

---

# 📱 Mobile Compatibility

The app supports:

* Android
* iPhone
* Desktop browsers

Special handling added for:

* Different text encodings
* ZIP uploads
* Mobile file upload compatibility

---

# 📊 Libraries Used & Why

| Library        | Why It Was Used                          |
| -------------- | ---------------------------------------- |
| streamlit      | To build the interactive web application |
| pandas         | To manage structured chat data           |
| matplotlib     | To create graphs and charts              |
| seaborn        | To generate heatmaps                     |
| wordcloud      | To visualize frequent words              |
| sklearn        | For topic modeling and ML tasks          |
| nltk           | For text preprocessing                   |
| vaderSentiment | For sentiment analysis                   |
| emoji          | To analyze emoji usage                   |
| urlextract     | To detect URLs shared in chats           |
| re             | For regex-based chat parsing             |

---

# 🖥️ Installation

## Clone Repository

```bash
git clone https://github.com/dba1808/whatsapp-chat-analyzer.git
```

---

## Navigate to Project Folder

```bash
cd whatsapp-chat-analyzer
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📦 requirements.txt

```bash
streamlit
pandas
matplotlib
seaborn
wordcloud
emoji
urlextract
scikit-learn
textblob
nltk
vaderSentiment
```

---

# 🌐 Deployment

This project is deployed using:

* Streamlit Community Cloud

Deployment process:

1. Push code to GitHub
2. Connect GitHub repository to Streamlit Cloud
3. Select `app.py`
4. Deploy application

Shockingly straightforward after surviving Docker deployment confusion.

---

# 📚 What I Learned

Through this project, I learned:

* Real-world data preprocessing
* NLP fundamentals
* Streamlit web app development
* Machine learning integration
* Data visualization techniques
* UI/UX improvements
* Deployment and debugging
* Mobile compatibility handling
* Privacy-focused preprocessing

Most importantly:
Building a project is one thing.
Making it usable by real people is a completely different challenge.

---

# 🔮 Future Improvements

Planned future features:

* Direct WhatsApp ZIP processing improvements
* Better multilingual summarization
* User authentication
* Export analysis as PDF
* Advanced AI chatbot integration
* Real-time chat insights

---

# 🙌 Acknowledgements

* Inspired during learning from CampusX
* Extended with additional NLP, UI, privacy, and analytics features

Learning from resources is normal.
Improving and extending them is where actual development begins.

---

# 📬 Feedback

Feedback and suggestions are always welcome.

If you found this project interesting, feel free to:

* Star the repository ⭐
* Share feedback
* Connect on LinkedIn

---

# 📄 License

This project is licensed under the MIT License.
