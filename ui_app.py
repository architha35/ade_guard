import streamlit as st
import requests

# --------------------- #
#  UI CONFIGURATION
# --------------------- #
st.set_page_config(
    page_title="ADEGuard Prototype",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 ADEGuard — AI-Powered ADE Analysis & Prediction")
st.markdown(
    "<p style='color:#996633; font-size:18px;'>Your intelligent assistant for analyzing and predicting vaccine side effects with real-time reassurance — ADE-Guard Now 🤖</p>",
    unsafe_allow_html=True
) 

# Backend URL (Flask)
BACKEND_URL = "http://127.0.0.1:5000"

# Tabs
tab1, tab2 = st.tabs(["💊 Post-Vaccine ADE Analysis", "💉 Pre-Vaccine Risk Prediction"])


# --------------------- #
#  TAB 1 — POST-VACCINE ANALYSIS
# --------------------- #
with tab1:
    st.subheader("💊 Post-Vaccine ADE Analysis")

    text_input = st.text_area(
        "Describe your symptoms after vaccination:",
        placeholder="Example: I have a fever and body pain since 2 days..."
    )

    vaccine_type = st.text_input("Vaccine name (optional):", placeholder="e.g. Pfizer, Moderna, Covaxin")

    if st.button("Analyze ADE Report"):
        if text_input.strip() == "":
            st.warning("⚠️ Please enter your symptom description.")
        else:
            with st.spinner("Analyzing report..."):
                try:
                    # Step 1: Send to /analyze
                    analyze_response = requests.post(
                        f"{BACKEND_URL}/analyze",
                        json={"text": text_input}
                    )

                    if analyze_response.status_code == 200:
                        analysis = analyze_response.json()
                        st.success("✅ Analysis Complete")
                        st.markdown(f"**Extracted Information:**\n```\n{analysis['model_output']}\n```")

                        # Step 2: Trigger reassurance (ADE-Guard Now)
                        reassure_response = requests.post(
                            f"{BACKEND_URL}/reassure",
                            json={
                                "symptom": text_input,
                                "vaccine": vaccine_type or "Unknown Vaccine"
                            }
                        )

                        if reassure_response.status_code == 200:
                            reassurance = reassure_response.json()
                            st.info(f"🤖 **ADE-Guard Now Says:**\n\n{reassurance['reassurance']}")
                        else:
                            st.warning("Reassurance engine temporarily unavailable.")

                    else:
                        st.error("⚠️ Error analyzing report. Please try again.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")


# --------------------- #
#  TAB 2 — PRE-VACCINE RISK PREDICTION
# --------------------- #
with tab2:
    st.subheader("💉 Pre-Vaccine Risk Prediction")

    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    conditions = st.text_area("Existing medical conditions (if any):", placeholder="e.g., diabetes, hypertension")
    allergies = st.text_area("Known allergies (if any):", placeholder="e.g., penicillin, pollen")
    vaccine = st.text_input("Vaccine Type", placeholder="e.g., Covaxin, Moderna")

    if st.button("Predict My Risk"):
        if gender == "Select" or not vaccine:
            st.warning("⚠️ Please fill all required fields.")
        else:
            with st.spinner("Predicting personalized risk..."):
                try:
                    # Step 1: Send to /predict
                    predict_response = requests.post(
                        f"{BACKEND_URL}/predict",
                        json={
                            "age": age,
                            "gender": gender,
                            "conditions": conditions,
                            "allergies": allergies,
                            "vaccine": vaccine
                        }
                    )

                    if predict_response.status_code == 200:
                        prediction = predict_response.json()
                        st.success("✅ Prediction Complete")
                        st.markdown(f"**AI Prediction:**\n```\n{prediction['prediction']}\n```")

                        # Step 2: Trigger reassurance (ADE-Guard Now)
                        reassure_prompt = f"expected mild reactions after {vaccine}"
                        reassure_response = requests.post(
                            f"{BACKEND_URL}/reassure",
                            json={
                                "symptom": reassure_prompt,
                                "vaccine": vaccine
                            }
                        )

                        if reassure_response.status_code == 200:
                            reassurance = reassure_response.json()
                            st.info(f"🤖 **ADE-Guard Now:**\n\n{reassurance['reassurance']}")
                        else:
                            st.warning("Reassurance engine temporarily unavailable.")

                    else:
                        st.error("⚠️ Error predicting risk. Please try again.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
