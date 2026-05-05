# IPL-Analytics-and-Win-Prediction
A data analytics and machine learning project that analyzes IPL cricket data using an interactive Streamlit dashboard and predicts match outcomes using an XGBoost model with advanced feature engineering.

# 🏏 IPL Analytics & Win Prediction System

Python
Streamlit
Machine Learning
Status
License

---

## 📌 Overview

This project is a Data Analytics + Machine Learning system built on IPL (Indian Premier League) cricket data.

It provides:
- 📊 Interactive analytics dashboard  
- 📈 Player & team performance insights  
- 🤖 Match win prediction using Machine Learning  

The goal is to combine data visualization and predictive modeling into a single application.

---

## 🚀 Features

### 🔎 Interactive Dashboard
- Team filter  
- Venue filter  
- Player search  

### 📊 KPI Metrics
- Total Runs  
- Total Matches  
- Total Wickets  
- Chasing Success Rate  

### 🏏 Batting Analysis
- Top 10 batsmen  
- Strike Rate vs Runs  

### 🎯 Bowling Analysis
- Top 10 bowlers  
- Economy vs Wickets  

### 📈 Team Analysis
- Most successful teams  
- Matches per venue  
- Season trends  

### 👤 Player Analysis
- Auto-detect batter / bowler  
- Detailed performance stats  

### ⚔️ Player Comparison
- Compare two players  

---

## 🤖 Machine Learning Model

- Model Used: XGBoost Classifier
- Problem Type: Classification (Match Winner Prediction)

### 🧠 Features Used
- Team Strength (Win %)
- Toss Advantage
- Head-to-Head Record
- Venue Performance

### 📊 Model Performance
- Accuracy: ~54%  
- Cross-validation: ~48%  

> ⚠️ Note: IPL prediction is inherently uncertain; performance is realistic for structured data.

---

## 📂 Dataset

### 1. Ball-by-Ball Dataset
Used for analytics and dashboard.
Dataset uploaded in zip format due to size limitations.

### 2. Match-Level Dataset
Used for ML model training.

Source: Kaggle IPL datasets

---

## 🛠️ Tech Stack

- Python  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  
- Streamlit  
- Scikit-learn  
- XGBoost  

---

## 🖥️ Project Structure

ipl-analytics-win-prediction/ │ ├── app.py ├── requirements.txt ├── README.md │ ├── data/ │   ├── ball_by_ball_ipl.csv │   └── ipl_matches.csv │ └── .venv/ (not included in repo)

---

## ⚙️ Setup & Installation

### 1. Clone Repository
bash git clone https://github.com/your-username/ipl-analytics-win-prediction.git cd ipl-analytics-win-prediction 

### 2. Create Virtual Environment
bash python3 -m venv .venv source .venv/bin/activate   # Mac/Linux 

### 3. Install Dependencies
bash pip install -r requirements.txt 

### 4. Run Application
bash streamlit run app.py 

---

## ⚠️ Challenges Faced

- Feature mismatch due to encoding  
- Low initial model accuracy  
- Debugging Streamlit errors  

---

## 🚀 Improvements Made

- Switched to XGBoost from Random Forest  
- Added advanced feature engineering  
- Improved UI with filters & KPI cards  
- Fixed player role detection  
- Added match insights in prediction  

---

## 📌 Future Scope

- Real-time data integration  
- Player-level prediction  
- Deep learning models  
- Web deployment  

---

## ⭐ If you like this project

Give it a ⭐ on GitHub
