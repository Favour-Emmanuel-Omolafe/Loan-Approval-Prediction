import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page configuration
st.set_page_config(
    page_title="Autonomous Credit Underwriting & Risk Prediction System",
    page_icon="🏦",
    layout="wide"
)

# Load the trained model pipeline
@st.cache_resource
def load_model():
    return joblib.load("credit_underwriting_pipeline.pkl")

model = load_model()

# App Header
st.title("🏦 Autonomous Credit Underwriting & Risk Prediction System")
st.markdown("Real-time retail credit risk evaluation and threshold-optimized default risk decision engine.")

st.markdown("---")

# User Input Form
st.sidebar.header("Applicant Financial Profile")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
married = st.sidebar.selectbox("Married", ["Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.sidebar.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.sidebar.selectbox("Self Employed", ["No", "Yes"])

applicant_income = st.sidebar.number_input("Applicant Income (Monthly)", min_value=0, value=50000)
coapplicant_income = st.sidebar.number_input("Coapplicant Income (Monthly)", min_value=0, value=0)
loan_amount = st.sidebar.number_input("Loan Amount (in thousands)", min_value=1, value=150)
loan_amount_term = st.sidebar.selectbox("Loan Amount Term (Months)", [360, 180, 240, 120, 60], index=0)
credit_history = st.sidebar.selectbox("Credit History (1 = Good, 0 = Bad)", [1.0, 0.0])
property_area = st.sidebar.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Main panel layout for prediction
if st.button("Evaluate Credit Risk"):
    # Create input dataframe matching training features
    input_data = pd.DataFrame({
        'Gender': [gender],
        'Married': [married],
        'Dependents': [dependents],
        'Education': [education],
        'Self_Employed': [self_employed],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Property_Area': [property_area]
    })
    
    # Run prediction through the pipeline
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)
    
    approval_prob = prediction_proba[0][1] # Probability of approval
    
    st.subheader("Underwriting Decision Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Model Confidence Score", f"{approval_prob * 100:.1f}%")
        
    with col2:
        if approval_prob >= 0.60:
            st.success("🟢 AUTOMATIC APPROVAL: Low default risk profile.")
        elif approval_prob >= 0.40:
            st.warning("🟡 MANUAL UNDERWRITER REVIEW: Borderline debt-to-income or credit profile.")
        else:
            st.error("🔴 AUTOMATIC REJECTION: High default probability exposure.")

    st.info("Note: Threshold policy automatically flags scores between 40% and 59% for human review to minimize asymmetric lending losses.")
