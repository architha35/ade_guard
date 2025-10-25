import pandas as pd
import re, json, requests
from collections import Counter

# -------- CONFIG --------
DATA_FILE = "./preprocessed/preprocessed_2025VAERSSYMPTOMS.csv"  # change if needed
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"
N_TOP_SYMPTOMS = 15

# -------- STEP 1: READ DATA --------
print(f"📊 Loading data from {DATA_FILE} ...")
df = pd.read_csv(DATA_FILE)

texts = df["report_text"].dropna().astype(str).tolist()[:1000]  # use sample for speed

# -------- STEP 2: SIMPLE PATTERN MINING --------
symptom_pattern = r"\b(headache|fever|pain|fatigue|nausea|chills|rash|vomiting|dizziness|soreness|swelling|cough|shortness of breath|myalgia|weakness)\b"
severity_pattern = r"\b(mild|moderate|severe|serious|life[- ]?threatening)\b"
duration_pattern = r"\b(\d+\s*(day|days|week|weeks|hour|hours))\b"

symptoms = Counter()
severity_terms = Counter()
durations = Counter()

for text in texts:
    symptoms.update(re.findall(symptom_pattern, text.lower()))
    severity_terms.update(re.findall(severity_pattern, text.lower()))
    durations.update(re.findall(duration_pattern, text.lower()))

top_symptoms = [s for s,_ in symptoms.most_common(N_TOP_SYMPTOMS)]
top_severities = [s for s,_ in severity_terms.most_common(5)]
top_durations = [s for s,_ in durations.most_common(5)]

# -------- STEP 3: BUILD BASE PROMPT --------
BASE_PROMPT = f"""
You are ADEGuard, an AI system trained on VAERS reports.
You analyze patient free-text reports and extract structured Adverse Drug Event (ADE) information.

Use these learned patterns from historical data:
- Common symptoms: {', '.join(top_symptoms)}
- Severity keywords: {', '.join(top_severities)}
- Duration indicators: {', '.join([d[0] for d in top_durations])}

Always return valid JSON with:
  "age", "symptoms", "severity", "duration", and "context" fields.
"""

print("✅ Context built successfully!\n")
print(BASE_PROMPT)

# -------- STEP 4: DEFINE FUNCTION TO QUERY MODEL --------
def query_ollama(prompt):
    data = {"model": MODEL_NAME, "prompt": prompt}
    r = requests.post(OLLAMA_API, json=data, stream=True)
    out = ""
    for chunk in r.iter_lines():
        if chunk:
            out += chunk.decode("utf-8")
    return out

# -------- STEP 5: TEST IT --------
test_input = "Patient aged 45 developed headache and fever for 2 days after vaccination."
final_prompt = f"{BASE_PROMPT}\n\nInput: {test_input}\nOutput:"

print("\n🧠 Sending test query to model...\n")
response = query_ollama(final_prompt)
print("💬 Model Response:\n", response)
