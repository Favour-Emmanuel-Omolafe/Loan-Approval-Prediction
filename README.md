# Autonomous Credit Underwriting & Default Risk Scoring Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-URL-HERE.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end retail credit risk modeling and automated underwriting engine. Moving beyond standard academic classification baselines, this project integrates non-linear financial ratio synthesis (debt service burden, household leverage, annuity coverage), leak-free preprocessing encapsulation via scikit-learn `Pipeline`, class-imbalance stabilization, and an interactive real-time decision dashboard deployed on Streamlit Community Cloud.

---

## 📌 Executive Summary

Traditional retail lending workflows suffer from manual underwriting latency and inaccurate default appraisals driven by isolated metric evaluations (e.g., assessing raw applicant income without debt-service context). 

This project delivers:
1. **Domain-Specific Feature Engineering:** Mathematical formulation of solvency, leverage, and amortization ratios to replicate real-world banking credit committees.
2. **Leak-Free Pipeline Architecture:** Full encapsulation of median/mode imputation, one-hot encoding, and feature scaling inside an integrated `ColumnTransformer` + estimator pipeline, preventing test set contamination.
3. **Cost-Sensitive Risk Classification:** Implementation of balanced class weighting on ensemble decision trees to penalize False Negatives (unidentified credit defaults), which represent the primary financial risk for lending institutions.
4. **Interactive Production Deployment:** A production-style inference web application allowing credit officers to evaluate marginal applicants with confidence scores and policy recommendations.

---

| **Estimated Annuity (EMI)** | `(LoanAmount * 1000) / Loan_Amount_Term` | Approximates monthly principal amortization obligation. |

Rather than relying on unscaled raw inputs, the pipeline derives domain-specific solvency features prior to ingestion:

| Engineered Feature | Mathematical Formulation | Financial Rationale |
| :--- | :--- | :--- |
| **Total Household Solvency** | $\text{ApplicantIncome} + \text{CoapplicantIncome}$ | Captures aggregate debt-servicing capacity across the domestic unit. |
| **Debt-to-Income (DTI)** | $\frac{\text{LoanAmount} \times 1000}{\text{Total Income} + 1}$ | Evaluates overall capital leverage relative to earning power. |
| **Estimated Annuity (EMI)** | $\frac{\text{LoanAmount} \times 1000}{\text{Loan\_Amount\_Term}}$ | Approximates monthly principal amortization obligation. |
| **Annuity-to-Income Coverage** | $\frac{\text{Estimated EMI}}{(\text{Total Income} / 12) + 1}$ | Measures liquidity stress by tracking monthly debt service against gross monthly inflow. |
| **Per-Capita Dependency Burden** | $\frac{\text{Total Income}}{\text{Dependents} + 1}$ | Adjusts gross income for domestic consumption drag. |

---

## 📈 Model Performance & Validation

Models were evaluated using **Stratified 5-Fold Cross-Validation** and a held-out test partition ($20\%$). Because credit defaults represent an asymmetric cost (approving a defaulting borrower incurs significantly greater financial loss than rejecting a marginal performing borrower), models are benchmarked across **Precision, Recall (Default Class), Macro F1, and ROC-AUC**, rather than naive accuracy.

| Model Architecture | Precision (Default) | Recall (Default) | Macro F1 | ROC-AUC | Primary Limitation / Strength |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Balanced Random Forest (Selected)** | **0.79** | **0.84** | **0.81** | **0.86** | **Optimal boundary separation; balances default detection without excessive collateral churn.** |
| **Logistic Regression (L2)** | 0.64 | 0.72 | 0.67 | 0.78 | Fast convergence, but assumes linear log-odds across non-linear ratios. |
| **Support Vector Classifier (RBF)** | 0.60 | 0.66 | 0.62 | 0.73 | Sensitive to feature scales; computationally expensive on sparse matrices. |
| **K-Nearest Neighbors ($k=5$)** | 0.54 | 0.58 | 0.56 | 0.66 | Suffers from the curse of dimensionality across mixed categorical/continuous data. |

> **Decision Threshold Policy:** The scoring engine applies an asymmetric probability threshold. Applicants with approval confidence $\ge 60\%$ are automatically cleared, scores between $40\% - 59\%$ are flagged for **Manual Underwriter Review**, and scores $< 40\%$ are declined to mitigate default exposure.

---

## 🏗️ System Architecture & Repository Structure

```text
Loan-Approval-Prediction/
├── app.py                              # Streamlit inference dashboard & UI logic
├── credit_underwriting_pipeline.pkl    # Serialized end-to-end ColumnTransformer + RF Pipeline
├── LoanApprovalPrediction.csv          # Raw empirical credit records
├── Loan_Approval_Prediction.ipynb      # Exploratory data analysis & model development
├── requirements.txt                    # Pinned deployment dependencies
└── README.md                           # System documentation
