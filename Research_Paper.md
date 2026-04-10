# Research Paper: Customer Engagement & Product Utilization Analytics for Retention Strategy

**Prepared For:** Unified Mentor / European Central Bank
**Domain:** Financial Analytics & Customer Retention

---

## 1. Abstract
This paper presents a behavioral analysis of bank customer churn, reframing retention strategies away from pure demographics towards engagement and product utilization. Utilizing a dataset of 10,000 customers from the European Bank across France, Spain, and Germany, the study isolates critical factors that actually dictate relationship stickiness and loyalty, exposing the myth that financial strength alone prevents churn.

## 2. Introduction & Problem Statement
Historically, retail banks have relied on balance volume and demographics to estimate customer lifetime value and likelihood of churn. However, systemic observation reveals that customers who appear financially robust often churn unexpectedly due to low engagement. 
The objective of this research is to:
1. Formulate engagement profiles and assess their corresponding churn probabilities.
2. Examine the impact of the bank's product offerings (Product Depth) on customer loyalty.
3. Establish behavioral KPIs to reshape institutional retention strategy.

---

## 3. Exploratory Data Analysis (EDA) Methodology

The provided dataset contains 14 initial features encompassing customer demographics (Geography, Gender, Age), account details (Balance, EstimatedSalary, CreditScore), and critical behavioral flags (IsActiveMember, NumOfProducts, HasCrCard).

### Data Preprocessing & Validation
- Validation confirmed no immediate missing values in core behavioral features.
- Categorical mappings (e.g., Exited mapping to Churned/Retained) were verified for distribution accuracy (approx ~20% baseline churn).

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

## 5. Strategic Recommendations

Based on empirical clustering and KPI derivation, we formally recommend the following tactical shifts:

1. **Implement an "At-Risk Premium" Dashboard:** 
   Utilize the High-Balance Disengagement Rate to flag accounts that have a balance above median but have shown 0 recent activity. Dispatch dedicated relationship managers to these accounts immediately, as they stand at a >31% probability of transferring assets to competitors.

2. **The "Pathway to Two" Campaign:**
   A massive portion of the bank's base sits on 1 product with high churn. Institute aggressive product bundling or no-fee second product acquisition initiatives to push this base into the 2-product tier, where churn plummets to 7.5%.

3. **Product Fatigue Audits:**
   Automatically audit any account moving to 3 or 4 products. It is highly probable these represent an internal risk vector or a technical classification error that causes systematic account failure.

## 6. Conclusion
By adopting the models provided in the Streamlit Dashboard, the European Bank can shift from a reactive demographic-churn model to a proactive, behavior-driven retention engine. Tracking the defined KPIs (Engagement Retention Ratio, Product Depth Index, High-Balance Disengagement Rate) guarantees highly efficient allocation of retention resources and improved overall lifetime value.
