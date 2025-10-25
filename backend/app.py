from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# ✅ Home route (fixes "404 Not Found" issue)
@app.route('/')
def home():
    return '''
        <h2>🩺 ADEGuard Backend is Running</h2>
        <p>Use the API endpoints below:</p>
        <ul>
            <li><b>POST /analyze</b> – Analyze ADE text reports</li>
            <li><b>POST /predict</b> – Pre-vaccine risk predictor</li>
            <li><b>POST /reassure</b> – Real-time reassurance engine</li>
        </ul>
        <p>Example:</p>
        <code>curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d '{"text": "I had fever after vaccination"}'</code>
    '''


# ✅ Route 1 — Analyze ADE text (existing functionality)
@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text_input = data.get("text", "")

    if not text_input:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": f"Extract ADE details from this text:\n{text_input}"}]
        )
        model_output = response['message']['content']
        return jsonify({
            "input_text": text_input,
            "model_output": model_output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 2 — Pre-vaccine risk predictor (added feature)
@app.route('/predict', methods=['POST'])
def predict_risk():
    data = request.get_json()
    age = data.get("age")
    gender = data.get("gender")
    conditions = data.get("conditions", "")
    allergies = data.get("allergies", "")
    vaccine = data.get("vaccine", "")

    prompt = (
        f"Given the following user details:\n"
        f"- Age: {age}\n- Gender: {gender}\n"
        f"- Health conditions: {conditions}\n"
        f"- Allergies: {allergies}\n"
        f"- Vaccine type: {vaccine}\n\n"
        f"Predict the likelihood and severity of Adverse Drug Events (ADEs). "
        f"Give a percentage risk and summarize common outcomes."
    )

    try:
        response = ollama.chat(model="phi3:mini", messages=[{"role": "user", "content": prompt}])
        model_output = response['message']['content']
        return jsonify({"input_data": data, "prediction": model_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 3 — Real-time reassurance engine (new feature)
@app.route('/reassure', methods=['POST'])
def reassure_user():
    data = request.get_json()
    symptom = data.get("symptom", "")
    vaccine = data.get("vaccine", "")

    if not symptom:
        return jsonify({"error": "Symptom not provided"}), 400

    reassurance_prompt = (
        f"A patient reports '{symptom}' after taking the {vaccine} vaccine. "
        f"Provide a calm, data-based reassurance message. "
        f"Example: 'Fever for 2 days after Vaccine X is common — 87% of people report this. "
        f"You’re fine 👍 If it lasts beyond 4 days, consult a doctor.'"
    )

    try:
        response = ollama.chat(model="phi3:mini", messages=[{"role": "user", "content": reassurance_prompt}])
        reassurance_message = response['message']['content']
        return jsonify({
            "input_symptom": symptom,
            "vaccine": vaccine,
            "reassurance": reassurance_message
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
