# Research Paper: Customer Engagement & Product Utilization Analytics for Retention Strategy

**Prepared For:** Unified Mentor / European Central Bank
**Domain:** Financial Analytics & Customer Retention
**Version:** 2.0 — ML-Enhanced

---

## 1. Abstract
This paper presents a behavioral analysis of bank customer churn, reframing retention strategies away from pure demographics towards engagement and product utilization. Utilizing a dataset of 10,000 customers from the European Bank across France, Spain, and Germany, the study isolates critical factors that actually dictate relationship stickiness and loyalty, exposing the myth that financial strength alone prevents churn. **Version 2.0 extends the analysis with predictive machine learning models**, per-customer risk scoring, and quantified model evaluation metrics.

## 2. Introduction & Problem Statement
Historically, retail banks have relied on balance volume and demographics to estimate customer lifetime value and likelihood of churn. However, systemic observation reveals that customers who appear financially robust often churn unexpectedly due to low engagement.
The objective of this research is to:
1. Formulate engagement profiles and assess their corresponding churn probabilities.
2. Examine the impact of the bank's product offerings (Product Depth) on customer loyalty.
3. Establish behavioral KPIs to reshape institutional retention strategy.
4. **Build a predictive ML model for automated churn forecasting and risk scoring.**
5. **Provide detailed customer segmentation insights across demographics and behavior.**

---

## 3. Exploratory Data Analysis (EDA) Methodology

The provided dataset contains 14 initial features encompassing customer demographics (Geography, Gender, Age), account details (Balance, EstimatedSalary, CreditScore), and critical behavioral flags (IsActiveMember, NumOfProducts, HasCrCard).

### Data Preprocessing & Validation
- Validation confirmed no immediate missing values in core behavioral features.
- Categorical mappings (e.g., Exited mapping to Churned/Retained) were verified for distribution accuracy (approx ~20% baseline churn).
- **Feature engineering:** Age bands, tenure cohorts, credit score bands, and Relationship Strength Index (RSI) were computed.

### Engagement Profiling
To study engagement empirically, customers were classified into specialized behavioral segments:
- **Active Engaged:** `IsActiveMember == 1` and `NumOfProducts > 1`
- **Active Low-Product:** `IsActiveMember == 1` and `NumOfProducts == 1`
- **Inactive High-Balance:** `IsActiveMember == 0` and `Balance > Median Balance`
- **Inactive Disengaged:** `IsActiveMember == 0` falling beneath the high-balance threshold.

---

## 4. Key Outcomes and Analytics Findings

### 4.1 The Engagement Retention Ratio
The generalized churn for "Active" vs. "Inactive" members presents a strong base case:
- **Active Member Churn:** 14.2%
- **Inactive Member Churn:** 26.8%

However, layered segmentation reveals the true dynamics:
- **Active Engaged** customers churn at a highly suppressed rate of **9.6%**.
- **Inactive High-Balance** customers (the premium, silent churn risk) exhibit the highest flight risk at **31.2%**. This highlights a total failure in retention strategies that assume high deposits equate to high satisfaction.

### 4.2 Product Depth Index & Stickiness
A nonlinear relationship exists between `NumOfProducts` and retention:
- **1 Product:** 27.7% Churn
- **2 Products:** 7.5% Churn (Optimum Relationship Strength)
- **3 Products:** 82.7% Churn
- **4 Products:** 100.0% Churn

**Interpretation:** Cross-selling a customer from 1 product to 2 products is the single most effective retention tactic the bank can deploy. Conversely, >2 products indicate significant anomalies—potentially distressed customers or artifacts of accounts undergoing progressive liquidation.

### 4.3 Credit Card Ownership
`HasCrCard` has a negligible standalone impact on retention, refuting common assumptions about credit products acting as lock-in mechanisms.

---

## 5. Predictive Machine Learning Model (New)

### 5.1 Model Selection & Training
A **Random Forest Classifier** was trained on the dataset using an 80/20 stratified train-test split. The model uses 10 engineered features derived from the original 14 columns, with categorical encoding applied to Geography and Gender.

**Hyperparameters:**
- `n_estimators`: 200
- `max_depth`: 10
- `min_samples_split`: 5
- `random_state`: 42

### 5.2 Model Evaluation Metrics

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.867 |
| **Precision** | 0.815 |
| **Recall** | 0.445 |
| **F1-Score** | 0.576 |
| **ROC-AUC** | 0.861 |

The model achieves strong discriminative power (AUC 0.861), with high precision ensuring that flagged at-risk customers are likely true positives. The moderate recall indicates some churners are missed, which is acceptable in a business context where false positives are more costly than false negatives for relationship manager deployment.

### 5.3 Feature Importance Rankings
The model identifies the following features as most predictive of churn:
1. **Age** — Strongest predictor; older customers show higher churn tendencies
2. **NumOfProducts** — Confirms the Product Depth Index findings
3. **Balance** — High balances in inactive accounts signal risk
4. **IsActiveMember** — Direct behavioral indicator
5. **Geography** — Regional retention patterns vary significantly (Germany highest churn)

### 5.4 Risk Scoring System
Each customer receives a **churn probability** (0–100%) and is assigned to a **risk tier**:
- **Critical (≥70%):** Immediate intervention required
- **High (40–70%):** Prioritized for relationship manager outreach
- **Medium (20–40%):** Monitored with periodic engagement checks
- **Low (<20%):** Standard retention protocols

---

## 6. Advanced Segmentation Insights (New)

### 6.1 Age Band Analysis
Customers aged 46–65 exhibit significantly higher churn rates compared to younger cohorts, correlating with life-stage transitions (retirement planning, asset reallocation).

### 6.2 Geography × Engagement Cross-Analysis
Germany shows the highest churn across all engagement profiles, suggesting market-specific competitive pressures beyond behavioral factors alone.

### 6.3 Tenure Cohort Patterns
Short-tenure customers (0–2 years) show elevated churn, indicating onboarding experience gaps. Long-tenure customers (8–10 years) demonstrate strong retention when combined with active engagement.

### 6.4 Credit Score Risk Heatmap
The interaction between credit score bands and engagement profiles reveals that credit score has minimal independent effect on churn — engagement status dominates the risk landscape regardless of creditworthiness.

---

## 7. Strategic Recommendations

Based on empirical clustering, ML predictions, and KPI derivation, we formally recommend the following tactical shifts:

1. **Implement an "At-Risk Premium" Dashboard:**
   Utilize the High-Balance Disengagement Rate to flag accounts that have a balance above median but have shown 0 recent activity. Dispatch dedicated relationship managers to these accounts immediately, as they stand at a >31% probability of transferring assets to competitors.

2. **The "Pathway to Two" Campaign:**
   A massive portion of the bank's base sits on 1 product with high churn. Institute aggressive product bundling or no-fee second product acquisition initiatives to push this base into the 2-product tier, where churn plummets to 7.5%.

3. **Product Fatigue Audits:**
   Automatically audit any account moving to 3 or 4 products. It is highly probable these represent an internal risk vector or a technical classification error that causes systematic account failure.

4. **Deploy ML-Driven Automated Alerts (New):**
   Integrate the trained Random Forest model into the bank's CRM system to provide real-time risk scoring. Flag customers whose probability crosses the 40% threshold for proactive outreach.

5. **Regional Retention Strategy (New):**
   Germany requires tailored retention initiatives given its consistently elevated churn rates across all engagement profiles. Consider market-specific loyalty programs and competitive benchmarking.

## 8. Conclusion
By adopting the models provided in the Streamlit Dashboard, the European Bank can shift from a reactive demographic-churn model to a proactive, behavior-driven retention engine. The integration of predictive ML models transforms descriptive analytics into prescriptive action — enabling automated risk scoring, quantified revenue-at-risk tracking, and systematic allocation of retention resources for maximum ROI.
