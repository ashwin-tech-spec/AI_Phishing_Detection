# 🛡️ AI-Powered Phishing Detection & Cyber Safety Platform

## 📌 Project Overview

The **AI-Powered Phishing Detection & Cyber Safety Platform** is a Streamlit-based cybersecurity application designed to help users identify potentially malicious and phishing-related websites.

The platform uses Machine Learning techniques to analyze URLs and website-related characteristics and provides a risk prediction with a confidence score.

It also includes clone/brand impersonation detection support, cybersecurity awareness content, quizzes, safety tips, and detection history.

---

## 🎯 Objectives

* Detect potentially phishing URLs using Machine Learning.
* Identify potential phishing/clone or brand-impersonation websites.
* Provide an easy-to-use cybersecurity interface.
* Display prediction results and AI confidence.
* Maintain a history of previously analyzed URLs.
* Improve user awareness about phishing and online safety.

---

## ✨ Features

### 🔗 1. URL Detection

Users can enter a website URL and analyze it using the trained phishing detection model.

The system provides:

* Likely Legitimate result
* Potential Phishing result
* AI confidence percentage
* Technical feature information

### 🌐 2. Clone / Brand Impersonation Detection

The platform analyzes website and domain characteristics to identify potential phishing or brand-impersonation websites.

The system uses features such as:

* URL characteristics
* Domain characteristics
* HTTPS status
* SSL information
* WHOIS domain age
* IP-related information
* Brand reference information

### 🧠 3. Cybersecurity Quiz

Users can test their knowledge about phishing and cybersecurity through an interactive quiz.

### 🛡️ 4. Safety Tips

Provides useful cybersecurity awareness tips to help users recognize and avoid phishing attacks.

### 📜 5. Detection History

Stores previously analyzed URLs locally and displays:

* URL
* Detection type
* Prediction
* Confidence
* Date and time

---

## 🤖 Machine Learning

The project uses **Random Forest Classifier** models for website-related detection.

The models are stored as serialized `.pkl` files using Joblib.

### Main Models

* `phishing_model.pkl` — URL phishing detection model
* `clone_website_model.pkl` — website phishing/impersonation-related detection model
* `clone_website_features.pkl` — feature list used by the clone website model
* `brands_reference.pkl` — brand reference information

> The clone website component is designed to identify potential phishing/brand impersonation risk using website and domain characteristics. It is not a pixel-perfect visual clone detector.

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Joblib
* SQLite
* HTML/CSS through Streamlit styling
* Git & GitHub

---

## 📂 Project Structure

```text
AI_Phishing_Detection/
│
├── app.py
├── requirements.txt
├── README.md
│
├── model/
│   ├── phishing_model.pkl
│   ├── clone_website_model.pkl
│   ├── clone_website_features.pkl
│   └── brands_reference.pkl
│
├── pages/
│   ├── 1_URL_Detection.py
│   ├── 2_Cyber_Quiz.py
│   ├── 3_Safety_Tips.py
│   ├── 4_History.py
│   └── 5_Clone_Website_Detection.py
│
├── utils/
│   ├── feature_extractor.py
│   ├── predictor.py
│   ├── clone_website_detector.py
│   └── database.py
│
├── database/
│   └── phishing_history.db
│
├── dataset/
│   └── Dataset files
│
└── assets/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ashwin-tech-spec/AI_Phishing_Detection.git
```

### 2. Open the project folder

```bash
cd AI_Phishing_Detection
```

### 3. Create a virtual environment

```bash
python -m venv venv312
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv312\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Run the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🔍 Example

A user can enter a URL such as:

```text
https://www.google.com
```

The system analyzes the URL and displays the prediction and confidence.

For demonstration purposes, a suspicious-looking domain can also be tested without opening it in a browser.

---

## 🔐 Cybersecurity Notice

This project is intended for **educational and defensive cybersecurity purposes**.

Users should not visit suspicious URLs simply to test them. URL analysis can be performed without opening the website.

Machine Learning predictions are probabilistic and should not be considered a guarantee that a website is completely safe or malicious.

---

## 🚀 Future Enhancements

Possible future improvements include:

* Advanced website content analysis
* HTML-based phishing detection
* Screenshot-based visual similarity detection
* Improved brand impersonation detection
* Real-time threat intelligence integration
* More cybersecurity awareness modules
* Improved model evaluation and monitoring
* Cloud deployment

---

## 👨‍💻 Project

**AI-Powered Phishing Detection & Cyber Safety Platform**

Built as an academic cybersecurity and Artificial Intelligence project.
