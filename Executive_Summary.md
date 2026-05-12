# Executive Summary: Engagement-Driven Retention Strategy (v2 — ML-Enhanced)

## Context
The European Central Bank sponsored an analytical deep-dive into customer retention patterns to address a growing systemic issue: banks are losing seemingly loyal or affluent customers to competitors because their existing retention models rely heavily on demographic data and ignore actual behavioral patterns.

## The Problem Highlighted
Despite high balances and salaries, a "silent churn" phenomenon exists wherein physically affluent customers exhibit low engagement, resulting in unexpected account closures.

## Key Findings
1. **The Inactive High-Balance Risk:**
   Our clustering analysis revealed that **"Inactive High-Balance"** customers have the highest churn rate of any financial cohort, staggering at **31.2%**. This completely debunks the myth that high balances guarantee customer loyalty.
2. **Engagement Trumps All:**
   Customers classified as **"Active Engaged"** (active members with multiple products) have a churn rate of just **9.6%**, which is roughly 2.5x lower than their disengaged counterparts.
3. **The Product "Sweet Spot":**
   Possessing a single product places a customer at high risk (27.7% churn). Up-selling a customer to a second product drastically reduces churn to 7.5%. However, having 3 or more products triggers a massive spike in churn, indicating potential "product fatigue" or a data artifact related to account liquidation phases.

## ML-Powered Enhancements (New)
4. **Predictive Churn Model:**
   A Random Forest Classifier trained on the dataset achieves **86.7% accuracy** and **0.861 ROC-AUC**, enabling automated per-customer churn probability scoring. Each customer now receives a risk tier (Low / Medium / High / Critical) for prioritized intervention.
5. **Feature Importance Analysis:**
   The ML model confirms that **Age**, **Number of Products**, and **Balance** are the strongest churn predictors — not credit score or estimated salary — reinforcing the behavioral thesis over demographic assumptions.
6. **Revenue at Risk Quantification:**
   Customers with ≥50% predicted churn probability collectively hold **€102.7M+ in deposits**, representing immediate revenue at risk if retention actions are not deployed.

## Advanced KPIs Introduced
- **Relationship Strength Index (RSI):** Composite score (0–100) combining tenure, product ownership, and activity status to measure relationship depth.
- **Customer Lifetime Value (CLV) Estimate:** Derived from balance, RSI, and tenure to quantify each customer's long-term value.
- **Revenue at Risk:** Aggregate balance exposure from customers predicted to churn.

## Strategic Recommendations
- **Targeted Re-engagement for Wealthy Accounts:** Traditional marketing assumes high-balance accounts are safe. We recommend deploying immediate "health-check" interactions and exclusive loyalty incentives geared specifically toward the `Inactive High-Balance` segment to stave off the 31.2% churn risk.
- **Strategic Cross-Selling (The 1-to-2 Strategy):** The data definitively proves the highest ROI in cross-selling lies in migrating single-product users to a two-product ecosystem.
- **Monitoring Product Overload:** Accounts with 3+ products show highly volatile behavior. The bank must implement "Product Utilization Reviews" to ensure customers aren't overwhelmed or adopting misaligned products.
- **ML-Driven Automated Alerts (New):** Deploy the predictive model in production to flag customers transitioning from Medium → High risk tier, enabling proactive outreach before churn occurs.

## Conclusion
Retention strategies must pivot from demographic assumptions to behavioral reality. The addition of predictive ML models transforms this from a descriptive analytics tool into a prescriptive retention engine, enabling the European Bank to systematically identify, score, and intervene with at-risk customers before value is lost.
