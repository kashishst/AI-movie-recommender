# AI-movie-recommender
# 🎬 AI Movie Recommendation System

An AI-based movie recommendation system that suggests movies based on user preferences like **genre, mood, and type** using **TF-IDF** and **cosine similarity**.

---

## 🚀 Features

- 🎭 Mood-based recommendations
- 🔍 Content-based filtering
- ⚡ Fast similarity search using TF-IDF
- 🌐 Full-stack application (React + Flask)
- ⭐ Sorted results by IMDB rating

---

## 🧠 How It Works

1. User selects **genre, mood, and type**
2. Frontend (React) sends data to backend (Flask)
3. Input is converted into text
4. Text → **TF-IDF vector**
5. Compared with movie dataset using **cosine similarity**
6. Top similar movies are selected
7. Results are sorted by rating
8. Recommendations are displayed to the user

---

## 🏗️ Tech Stack

### Frontend
- React.js

### Backend
- Flask (Python)

### Machine Learning
- Scikit-learn (TF-IDF, cosine similarity)
- TensorFlow / Keras (Neural Network)

---
## 📂 Project Structure
project/
│── model.py # ML model & recommendation logic
│── app.py # Flask API
│── movies_cleaned.csv # Dataset
│── vectorizer.pkl # Saved TF-IDF model
│── encoder.pkl # Label encoder
│── movie_model.keras # Trained neural network
│
└── frontend/
├── src/App.js # React UI
└── App.css



