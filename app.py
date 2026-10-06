import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
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
def build_and_train_pipeline():
  # 1. Load empirical training data
  df = pd.read_csv("LoanApprovalPrediction.csv")

  # 2. Financial Feature Engineering
  df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
  df["Loan_to_Income_Ratio"] = (df["LoanAmount"] * 1000) / (
      df["Total_Income"] + 1
  )
  df["Estimated_EMI"] = (df["LoanAmount"] * 1000) / df[
      "Loan_Amount_Term"
  ].replace(0, np.nan)
  df["Annuity_to_Income_Ratio"] = df["Estimated_EMI"] / (
      (df["Total_Income"] / 12) + 1
  )
  df["Dependents_Clean"] = (
      df["Dependents"].replace("3+", 3).fillna(0).astype(float)
  )
  df["Income_Per_Capita"] = df["Total_Income"] / (df["Dependents_Clean"] + 1)

  numeric_features = [
      "ApplicantIncome",
      "CoapplicantIncome",
      "LoanAmount",
      "Total_Income",
      "Loan_to_Income_Ratio",
      "Estimated_EMI",
      "Annuity_to_Income_Ratio",
      "Income_Per_Capita",
  ]

  categorical_features = [
      "Gender",
      "Married",
      "Education",
      "Self_Employed",
      "Property_Area",
      "Credit_History",
  ]

  # 3. Transformers
  numeric_transformer = Pipeline(
      steps=[
          ("imputer", SimpleImputer(strategy="median")),
          ("scaler", StandardScaler()),
      ]
  )

  categorical_transformer = Pipeline(
      steps=[
          ("imputer", SimpleImputer(strategy="most_frequent")),
          ("onehot", OneHotEncoder(handle_unknown="ignore")),
      ]
  )

  preprocessor = ColumnTransformer(
      transformers=[
          ("num", numeric_transformer, numeric_features),
          ("cat", categorical_transformer, categorical_features),
      ]
  )

  pipeline = Pipeline(
      steps=[
          ("preprocessor", preprocessor),
          (
              "classifier",
              RandomForestClassifier(
                  n_estimators=150,
                  max_depth=6,
                  class_weight="balanced",
                  random_state=42,
              ),
          ),
      ]
  )

  X = df[numeric_features + categorical_features]
  y = df["Loan_Status"].map({"Y": 1, "N": 0})
  pipeline.fit(X, y)
  return pipeline


pipeline = build_and_train_pipeline()

with st.form("underwriting_form"):
  st.subheader("Applicant & Financial Profile")
  c1, c2 = st.columns(2)

  with c1:
    applicant_income = st.number_input(
        "Applicant Monthly Income ($)", min_value=0, value=5000, step=500
    )
    coapplicant_income = st.number_input(
        "Co-Applicant Monthly Income ($)", min_value=0, value=1500, step=500
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
