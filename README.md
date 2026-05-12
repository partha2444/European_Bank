# European Central Bank - Retention Analytics Dashboard (Pro)

## Overview
This project provides a comprehensive **Customer Engagement and Product Utilization Analytics** dashboard for the European Central Bank. It combines behavior-driven exploratory analysis with **predictive machine learning models** to deliver automated churn forecasting, per-customer risk scoring, and actionable retention insights.

The dashboard moves beyond traditional demographic-based churn models by integrating a Random Forest classifier, advanced KPIs (CLV, RSI, Revenue at Risk), and deep segmentation analysis.

## Key Features

### Predictive ML Engine
- **Random Forest Classifier** trained on the full dataset with 80/20 stratified split
- **Per-customer churn probability** (0–100%) and automated **risk tier assignment** (Low/Medium/High/Critical)
- **Model evaluation metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Interactive **ROC Curve**, **Confusion Matrix**, and **Feature Importance** charts

### Advanced KPIs
- **Overall / Active / Inactive Churn Rates** — segmented departure tracking
- **Revenue at Risk** — total balance held by customers with ≥50% churn probability
- **Relationship Strength Index (RSI)** — composite score (tenure, products, activity) per customer
- **Customer Lifetime Value (CLV)** estimation
- **Premium Inactive Churn** — targeted high-balance disengaged flight risk

### Interactive Dashboard (6 Tabs)
1. **Engagement vs Churn** — Churn rate by behavioral profile, active/inactive split
2. **Product Utilization** — Product depth vs. churn, credit card stickiness analysis
3. **High-Value Detection** — Scatter landscape of at-risk premium accounts with detailed table
4. **ML Predictions** — Model metrics, ROC curve, confusion matrix, feature importance, risk distribution
5. **Segmentation Deep-Dive** — Age band, geography × engagement, tenure cohort, gender × product, and credit score heatmap analyses
6. **Reports** — Downloadable CSV exports (filtered data, at-risk customers, full predictions) and PDF executive report

### Engagement Profiling
- **Active Engaged** — Active members with multiple products
- **Inactive High-Balance** — Inactive with above-median balance (31.2% churn — the "silent churn" risk)
- **Active Low-Product** — Active but single-product users
- **Inactive Disengaged** — Low engagement, low balance

## Repository Contents
| File | Description |
|------|-------------|
| `app.py` | Main Streamlit dashboard with ML integration |
| `ml_engine.py` | Standalone ML module (training, evaluation, risk scoring) |
| `eda.py` | Initial exploratory data analysis script |
| `Executive_Summary.md` | Stakeholder-facing summary of findings and recommendations |
| `Research_Paper.md` | Detailed methodology and analytical findings |
| `requirements.txt` | Project dependencies |
| `European_Bank.csv` | Customer dataset (10,000 records, 14 features) |

## Installation and Usage

1. **Navigate to the project directory:**
   ```bash
   cd European_Bank
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**
   ```bash
   python -m streamlit run app.py
   ```

4. **Access the Application:**
   Open your browser at `http://localhost:8501`

## Tech Stack
- **[Streamlit](https://streamlit.io/)** — Interactive web application framework
- **[Pandas](https://pandas.pydata.org/)** & **[NumPy](https://numpy.org/)** — Data manipulation
- **[Plotly](https://plotly.com/)** — Interactive, responsive visualizations
- **[scikit-learn](https://scikit-learn.org/)** — Machine learning models and evaluation
- **[fpdf2](https://py-pdf.github.io/fpdf2/)** — PDF report generation

## Strategic Insights
- High balances do **not** guarantee loyalty — 31.2% churn for Inactive High-Balance accounts
- Active engagement + 2 products reduces churn to ~7.5%
- The ML model achieves **0.86 ROC-AUC**, with Age and Balance as top predictive features
- **Revenue at Risk** quantifies the financial impact of predicted churners

## Built With
Unified Mentor • European Central Bank Retention Division Analytics
