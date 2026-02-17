import streamlit as st
import joblib
import numpy as np
import pandas as pd

model = joblib.load('credit_risk_model.pkl')
st.title("💳 Kredit Risk Bashorati")
st.write("Quyidagi ma'lumotlarni kiriting:")

col1, col2 = st.columns(2)

with col1:
    person_age = st.number_input("Yosh", min_value=18, max_value=100, value=30)
    person_income = st.number_input("Yillik daromad ($)", min_value=0, value=50000)
    person_emp_length = st.number_input("Ish tajribasi (yil)", min_value=0.0, max_value=50.0, value=5.0)
    loan_amnt = st.number_input("Kredit miqdori ($)", min_value=0, value=10000)
    loan_int_rate = st.number_input("Foiz stavkasi (%)", min_value=0.0, max_value=30.0, value=10.0)
    cb_person_cred_hist_length = st.number_input("Kredit tarixi (yil)", min_value=0, max_value=50, value=5)

with col2:
    loan_grade = st.selectbox("Kredit reytingi", ["A", "B", "C", "D", "E", "F", "G"])
    loan_intent = st.selectbox("Kredit maqsadi", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
    person_home_ownership = st.selectbox("Uy egaligi", ["RENT", "MORTGAGE", "OWN", "OTHER"])
    cb_person_default_on_file = st.selectbox("Oldin default bo'lganmi?", ["N", "Y"])

loan_percent_income = loan_amnt / person_income if person_income > 0 else 0
st.write(f"Kreditning daromadga nisbati: **{loan_percent_income:.2f}**")

if st.button("Bashorat qilish"):
    # Loan grade encode
    grade_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    loan_grade_enc = grade_map[loan_grade]

    # Loan intent encode
    intent_map = {"DEBTCONSOLIDATION": 0, "EDUCATION": 1, "HOMEIMPROVEMENT": 2, "MEDICAL": 3, "PERSONAL": 4, "VENTURE": 5}
    loan_intent_enc = intent_map[loan_intent]

    # Home ownership dummies
    home_MORTGAGE = 1 if person_home_ownership == "MORTGAGE" else 0
    home_OTHER = 1 if person_home_ownership == "OTHER" else 0
    home_OWN = 1 if person_home_ownership == "OWN" else 0
    home_RENT = 1 if person_home_ownership == "RENT" else 0

    # Default on file dummies
    default_N = 1 if cb_person_default_on_file == "N" else 0
    default_Y = 1 if cb_person_default_on_file == "Y" else 0

    input_data = pd.DataFrame([[
        person_age, person_income, person_emp_length,
        loan_intent_enc, loan_grade_enc, loan_amnt,
        loan_int_rate, loan_percent_income, cb_person_cred_hist_length,
        home_MORTGAGE, home_OTHER, home_OWN, home_RENT,
        default_N, default_Y
    ]], columns=X.columns if 'X' in dir() else [
        'person_age', 'person_income', 'person_emp_length',
        'loan_intent', 'loan_grade', 'loan_amnt',
        'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length',
        'person_home_ownership_MORTGAGE', 'person_home_ownership_OTHER',
        'person_home_ownership_OWN', 'person_home_ownership_RENT',
        'cb_person_default_on_file_N', 'cb_person_default_on_file_Y'
    ])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Kredit XAVFLI! Qaytarmaslik ehtimoli: {probability:.1%}")
    else:
        st.success(f"✅ Kredit XAVFSIZ! Qaytarmaslik ehtimoli: {probability:.1%}")