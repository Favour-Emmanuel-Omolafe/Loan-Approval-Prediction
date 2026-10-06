import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Credit Underwriting & Risk Engine", layout="centered"
)

st.title("Credit Underwriting & Risk Decision Engine")
st.write(
    "Production-grade scoring pipeline using financial ratio engineering,"
    " leak-free transformers, and class-balanced Random Forest classification."
)


@st.cache_resource
def load_pipeline():
  return joblib.load("credit_underwriting_pipeline.pkl")


pipeline = load_pipeline()

with st.form("underwriting_form"):
  st.subheader("Applicant & Financial Profile")
  c1, c2 = st.columns(2)

  with c1:
    applicant_income = st.number_input(
        "Applicant Monthly Income ($)",
        min_value=0,
        value=5000,
        step=500,
    )
    coapplicant_income = st.number_input(
        "Co-Applicant Monthly Income ($)",
        min_value=0,
        value=1500,
        step=500,
    )
    loan_amount = st.number_input(
        "Loan Amount (in Thousands $)", min_value=1, value=120, step=10
    )
    loan_term = st.selectbox(
        "Loan Term (Months)", [120, 180, 240, 300, 360], index=4
    )

  with c2:
    credit_history = st.selectbox(
        "Credit Bureau Compliance",
        options=[1.0, 0.0],
        format_func=lambda x: (
            "Meets Credit Guidelines (1.0)"
            if x == 1.0
            else "Prior Delinquencies / Defaults (0.0)"
        ),
    )
    education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
    married = st.selectbox("Marital Status", ["Yes", "No"])
    property_area = st.selectbox(
        "Property Zone", ["Urban", "Semiurban", "Rural"]
    )
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])
    gender = st.selectbox("Gender", ["Male", "Female"])

  submitted = st.form_submit_button("Assess Credit Risk")

if submitted:
  total_income = applicant_income + coapplicant_income
  loan_to_income = (loan_amount * 1000) / (total_income + 1)
  monthly_emi = (loan_amount * 1000) / loan_term
  annuity_to_income = monthly_emi / ((total_income / 12) + 1)
  dep_num = 3.0 if dependents == "3+" else float(dependents)
  income_per_capita = total_income / (dep_num + 1)

  input_data = pd.DataFrame([{
      "ApplicantIncome": applicant_income,
      "CoapplicantIncome": coapplicant_income,
      "LoanAmount": loan_amount,
      "Total_Income": total_income,
      "Loan_to_Income_Ratio": loan_to_income,
      "Estimated_EMI": monthly_emi,
      "Annuity_to_Income_Ratio": annuity_to_income,
      "Income_Per_Capita": income_per_capita,
      "Gender": gender,
      "Married": married,
      "Education": education,
      "Self_Employed": self_employed,
      "Property_Area": property_area,
      "Credit_History": credit_history,
  }])

  prob_approval = pipeline.predict_proba(input_data)[0, 1]
  prob_default = 1.0 - prob_approval

  st.divider()
  st.subheader("Risk Assessment & Underwriting Verdict")

  col_m1, col_m2 = st.columns(2)
  col_m1.metric("Calculated Default Risk", f"{prob_default * 100:.1f}%")
  col_m2.metric("Approval Probability", f"{prob_approval * 100:.1f}%")

  if prob_approval >= 0.60:
    st.success(
        "**Decision: Approved (Low Risk).** Financial ratios and credit"
        " compliance satisfy solvency requirements."
    )
  elif prob_approval >= 0.40:
    st.warning(
        "**Decision: Refer to Manual Underwriting.** Elevated debt-to-income"
        " or borderline collateral metrics detected."
    )
  else:
    st.error(
        "**Decision: Declined (High Risk).** High default probability based on"
        " historical delinquency patterns."
    )
