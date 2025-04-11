# Quamus – Chatbot-Based Course Recommendation System 🎓💬

**Quamus** is an intelligent, machine-learning-driven course recommendation system that helps users discover relevant online courses. By leveraging NLP techniques and data from top MOOC platforms like Coursera, edX, and Udemy, Quamus provides personalized course recommendations based on users' learning preferences and goals, through an intuitive chatbot interface.

## 🚀 Features

- **Data Collection**: Scrapes course metadata from Coursera, edX, and Udemy using Scrapy and Playwright.
- **Data Preprocessing**: Cleans and normalizes course information; course descriptions are embedded using SBERT (Sentence-BERT) for semantic similarity.
- **Content-Based Recommendation**: Provides personalized course suggestions based on semantic similarity, adapting over time with user interaction.
- **Two-Tower Model**: Utilizes a dual-encoder architecture to learn user-item embeddings, trained on pseudo-labels derived from course content.
- **Transformer Architecture (WIP)**: A custom transformer model designed to predict the next course in a user's learning journey (currently under development).
- **Conversational Interface**: Integrates the Gemini API to facilitate contextual interactions and provide relevant, dynamic recommendations through a chatbot interface.

---

## 🧠 Tech Stack

- **Programming Language**: Python
- **Web Scraping**: Scrapy, Playwright
- **NLP & Embeddings**: Sentence-BERT (SBERT)
- **Machine Learning Models**: Scikit-learn, PyTorch (Two-Tower + Transformer)
- **Chatbot API**: Gemini API (Google)
- **Recommendation Logic**: Hybrid content-based filtering with user-adaptive techniques

---

## 📚 Example Use Case

**User Query**:  
> 🗨️ _"I'm looking for a beginner-friendly course in data analysis with Python."_

**Quamus Response**:  
> ✅ Quamus replies with:
> - “Data Analysis with Python – Coursera”
> - “The Data Science Course 2024 – Udemy”
> - “Data Wrangling and Visualization – edX”

---

## 🛠️ Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/karar-git/Quamus.git
cd quamus
```

### 2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install discover them ur self
```

### 3. Set your **Gemini API** key:
Go to models/chatbot.py
```

### 4. Run the chatbot:
```bash
python chatbot.py
```

---
## 🧪 Disclaimer

- **Educational Purpose**: The course data scraping from platforms like Coursera, edX, and Udemy is done strictly for educational and research purposes. This project is not intended for commercial use, and we encourage users to respect the terms and conditions of the respective platforms.
- **Scraping Limitations**: The scraping scripts are designed to collect course metadata and do not store or share any personal or proprietary information from users or the platforms. Please use responsibly.
---

## 🧪 Future Plans

- **Transformer-based Course Predictor**: Complete the development and training of the transformer model to predict the next course based on user learning progression.
- **Resource Expansion**: Extend recommendations to include books, articles, and videos tailored to the user’s learning path.
- **Connect the Two-Tower Model with the GUI**: Currently, only the cosine similarity model is connected and working, without personalization. Connecting the two-tower model to the GUI should be straightforward, but it remains on the to-do list for now.
- **Long-term Personalization**: Improve recommendations by tracking long-term learning patterns and incorporating continuous feedback from users.

---

## 📄 License

GPL License

---

## 👨‍💻 Authors

Teeba Nazar on the GUI
[LinkedIn](https://www.linkedin.com/in//) • [GitHub](https://github.com/teeba3/)

Karar Haitham for the Recommendation system, Data Scraping, and Preprocessing
[LinkedIn](https://www.linkedin.com/in/karar-haitham-6808b535b/) • [GitHub](https://github.com/karar-git/)
