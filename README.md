# 🩺 ADEGuard — AI-Powered Vaccine ADE Analysis & Prediction

ADEGuard is an AI-driven healthcare assistant that analyzes and predicts **Adverse Drug Events (ADEs)** related to vaccinations — while also providing **real-time reassurance** to users through a feature called **“ADE-Guard Now”** 🧠💬.

Built as part of a **hackathon project**, this system combines predictive analytics, symptom understanding, and empathetic AI communication — to reduce vaccine anxiety and improve trust in public health.

---

## 🚀 Features

### 💊 Post-Vaccine ADE Analysis
- Users describe their symptoms after vaccination.
- The system extracts:
  - Symptoms
  - Duration
  - Severity
  - Possible ADE category  
- Returns structured AI output and instant reassurance feedback.

### 💉 Pre-Vaccine Risk Prediction
- Users input:
  - Age, Gender
  - Existing Conditions
  - Allergies
  - Vaccine Type
- Predicts the **likelihood of mild/moderate/severe reactions**.
- Provides **preventive guidance** and reassurance messages like:
  > “80% of people like you report mild fever for 2 days after this vaccine. Low risk of serious reaction.”

### 🤖 ADE-Guard Now — Real-Time Reassurance Engine
- Offers calm, personalized, and data-backed reassurance:
  > “Fever for 2 days after Vaccine X is completely normal — 87% of people report this. You’re fine 👍.”
- Built using **LLM (Ollama)** integrated with Flask and Streamlit frontend.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit (Python) |
| **Backend** | Flask |
| **LLM Engine** | Ollama (local Phi-3 or similar model) |
| **Language** | Python 3.10+ |
| **Styling** | Custom Streamlit UI with warm color palette |

---

## 🗂️ Project Structure

ADE_Guard/
│
├── backend/
│ ├── app.py # Flask backend with endpoints
│ ├── reassurance_engine.py # Real-time reassurance logic
│ ├── requirements.txt # Dependencies
│
├── ui_app.py # Streamlit Frontend UI
└── README.md

---

## ⚙️ Setup Instructions

### 
1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/ADEGuard.git
cd ADEGuard/backend
```
2️⃣ Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # Mac
``` 
3️⃣ Run the Flask backend
```
python3 app.py
```
4️⃣ Run the Streamlit frontend

```
streamlit run ui_app.py
```

🎨 UI Preview
<img width="2940" height="1912" alt="Image 25-10-25 at 5 22 PM" src="https://github.com/user-attachments/assets/c429a877-69e4-403f-a5bb-a8048724bf0e" />
<img width="2766" height="1502" alt="Image 25-10-25 at 5 23 PM" src="https://github.com/user-attachments/assets/5dfa7f57-2af1-400d-95ae-183137f192c8" />
<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/63962595-7383-4d4d-8655-9ab24337c4ce" />

 👩‍💻 Author
 
Architha : https://github.com/architha35
Linkedin : https://www.linkedin.com/in/architha-reddy-3190132ba/



