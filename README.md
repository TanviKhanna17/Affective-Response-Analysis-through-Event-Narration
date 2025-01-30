# Affective Response Analysis for Understanding Emotion Quotient through Event Narration  

## 📌 Overview  
This project aims to analyze and quantify user emotions in interactive storytelling using Natural Language Processing (NLP) and Machine Learning (ML). By tracking emotional responses across multiple sessions, it provides insights into user engagement, sentiment evolution, and decision-making patterns.  

---

## 🚀 Features  
- **Emotion Tracking:** Uses transformer-based NLP models to classify emotions from textual input.  
- **Multi-Session Analysis:** Captures how user emotions evolve over multiple interactions.  
- **Textual Relevance Mapping:** Employs cosine similarity to measure the contextual alignment of user feedback with story events.  
- **Quantitative Emotional Impact:** Computes emotion intensity and tracks indecisiveness through response changes.  
- **Data Visualization:** Generates interactive charts for analyzing emotional trajectories.  

---

## 🛠️ Tech Stack  

| Component         | Technology Used  |
|------------------|----------------|
| **Programming Language** | Python  |
| **Backend Framework** | Flask / Django  |
| **Database** | MySQL / PostgreSQL  |
| **Frontend** | React.js  |
| **NLP Models** | RoBERTa, ALBERT, LSTM-GloVe  |
| **Data Processing** | Pandas, NumPy, NLTK, Scikit-learn  |
| **Visualization** | Matplotlib, Seaborn, Plotly  |

---

## 🏗️ System Architecture  

The system consists of three major modules:  

### 1️⃣ **Data Collection & Preprocessing**  
- **Data Source:** User textual feedback on predefined story events.  
- **Preprocessing Steps:**  
  - Tokenization using BERT-based tokenizers.  
  - Stopword removal and stemming (NLTK).  
  - Handling contractions and slang using a custom dictionary.  
  - Converting emojis to text representations using `emoji` library.  

### 2️⃣ **Emotion Classification & Relevance Mapping**  
- **Models Used:**  
  - **RoBERTa:** Most accurate model for textual emotion classification (~92.3% accuracy).  
  - **ALBERT:** Optimized for efficiency with shared layers and factorized embeddings.  
  - **LSTM-GloVe:** Baseline sequential model for comparison.  
- **Emotion Scoring:**  
  - Each feedback is mapped to 13 distinct emotion categories (happiness, sadness, anger, etc.).  
  - Cosine similarity is used to measure the contextual relevance of feedback to the event.  

### 3️⃣ **Session Management & Emotion Evolution Analysis**  
- **Database Schema:**  
  - `Users`: Stores user details and interaction history.  
  - `Events`: Predefined narrative elements triggering emotional responses.  
  - `Sessions`: Tracks each user’s engagement, storing their emotional journey.  
  - `Emotional_Analysis`: Stores computed emotion scores for each feedback instance.  
- **Multi-Session Analysis:**  
  - Identifies patterns in how user emotions shift over time.  
  - Tracks hesitation and indecisiveness based on response modifications.  
