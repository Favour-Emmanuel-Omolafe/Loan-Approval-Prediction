import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Credit Underwriting Engine", layout="centered")

@st.cache_resource
def train_and_get_model():
    # Load dataset
    data = pd.read_csv("LoanApprovalPrediction.csv")
    if 'Loan_ID' in data.columns:
        data.drop(['Loan_ID'], axis=1, inplace=True)
    
    # Domain Feature Engineering (matching notebook cell [9])
    data['Total_Income'] = data['ApplicantIncome'] + data['CoapplicantIncome'].fillna(0)
    data['DTI'] = (data['LoanAmount'] * 1000) / (data['Total_Income'] + 1)
    term = data['Loan_Amount_Term'].fillna(360)
    data['Estimated_EMI'] = (data['LoanAmount'] * 1000) / term
    data['Annuity_Coverage'] = data['Estimated_EMI'] / ((data['Total_Income'] / 12) + 1)
    data['Dependents'] = data['Dependents'].fillna(0)

    # Impute missing numeric values
    data['LoanAmount'] = data['LoanAmount'].fillna(data['LoanAmount'].median())
    data['Loan_Amount_Term'] = data['Loan_Amount_Term'].fillna(360)
    data['Credit_History'] = data['Credit_History'].fillna(1.0)

    # Categorical mapping (matching notebook cell [10])
    mapping = {
        'Gender': {'Male': 1, 'Female': 0},
        'Married': {'Yes': 1, 'No': 0},
        'Education': {'Graduate': 0, 'Not Graduate': 1},
        'Self_Employed': {'Yes': 1, 'No': 0},
        'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2}
    }
    for col, m in mapping.items():
        if col in data.columns:
            data[col] = data[col].map(m).fillna(0)

    # Encode target
    Y = data['Loan_Status'].map({'Y': 1, 'N': 0})
    X = data.drop(['Loan_Status'], axis=1)

    # Train Balanced Random Forest
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf.fit(X, Y)
    return rf, list(X.columns)

# Train or retrieve model from cache
model, feature_cols = train_and_get_model()

st.title("🏦 Autonomous Credit Underwriting Engine")
st.markdown("Automated retail credit risk assessment and solvency classification.")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", [0.0, 1.0, 2.0, 3.0])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

with col2:
    applicant_income = st.number_input("Applicant Income ($/mo)", min_value=0.0, value=5000.0)
    coapplicant_income = st.number_input("Co-Applicant Income ($/mo)", min_value=0.0, value=1500.0)
    loan_amount = st.number_input("Loan Amount (Thousands $)", min_value=1.0, value=120.0)
    loan_term = st.selectbox("Loan Term (Months)", [360.0, 180.0, 240.0, 120.0])
    credit_history = st.selectbox("Credit History", [1.0, 0.0], format_func=lambda x: "Good (1.0)" if x == 1.0 else "Defaulter / None (0.0)")

if st.button("Evaluate Credit Risk", type="primary"):
    total_income = applicant_income + coapplicant_income
    dti = (loan_amount * 1000) / (total_income + 1)
    estimated_emi = (loan_amount * 1000) / loan_term
    annuity_coverage = estimated_emi / ((total_income / 12) + 1)

    mapping = {
        'Gender': {'Male': 1, 'Female': 0},
        'Married': {'Yes': 1, 'No': 0},
        'Education': {'Graduate': 0, 'Not Graduate': 1},
        'Self_Employed': {'Yes': 1, 'No': 0},
        'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2}
    }

    input_df = pd.DataFrame([{
        'Gender': mapping['Gender'][gender],
        'Married': mapping['Married'][married],
        'Dependents': float(dependents),
        'Education': mapping['Education'][education],
        'Self_Employed': mapping['Self_Employed'][self_employed],
        'ApplicantIncome': applicant_income,
        'CoapplicantIncome': coapplicant_income,
        'LoanAmount': loan_amount,
        'Loan_Amount_Term': loan_term,
        'Credit_History': float(credit_history),
        'Property_Area': mapping['Property_Area'][property_area],
        'Total_Income': total_income,
        'DTI': dti,
        'Estimated_EMI': estimated_emi,
        'Annuity_Coverage': annuity_coverage
    }])[feature_cols]

    prob = model.predict_proba(input_df)[0][1]

    st.write("---")
    st.metric(label="Approval Probability", value=f"{prob * 100:.1f}%")

    if prob >= 0.60:
        st.success("✅ **APPROVED**: Meets solvency criteria.")
    elif prob >= 0.40:
        st.warning("⚠️ **MANUAL UNDERWRITING REQUIRED**: Marginal risk boundary.")
    else:
        st.error("❌ **DECLINED**: High risk of default.")
