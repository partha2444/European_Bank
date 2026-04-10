# European Central Bank - Retention Analytics Dashboard

## Overview
This project provides a comprehensive Customer Engagement and Product Utilization Analytics dashboard for the European Central Bank. The primary objective is to move beyond traditional demographic-based churn models by developing a behavior-driven retention strategy. 

Through exploratory data analysis and predictive modeling, this project identifies high-risk customer segments—specifically "Inactive High-Balance" accounts—often overlooked by traditional systems but representing significant "silent churn" risk. 

## Key Features
- **Exploratory Data Analysis (EDA):** In-depth analysis (`eda.py`) uncovering the relationship between customer engagement profiles, product utilization, and churn ("Exited" status).
- **Interactive Dashboard:** A professional Streamlit web application (`app.py`) visualizing key insights, churn rates by engagement profile, and deep-dives into at-risk cohorts.
- **Engagement Profiling:** Categorizes users into distinct behavioral profiles (e.g., Active Engaged, Inactive High-Balance, Active Low-Product) to provide actionable retention targets.
- **At-Risk Premium Cohort Detection:** Specifically highlights affluent customers who are disengaged and present an immediate churn risk.

## Repository Contents
- `app.py`: The main Streamlit application script for the retention analytics dashboard.
- `eda.py`: Exploratory Data Analysis script used for initial data profiling and modeling.
- `Executive_Summary.md`: A high-level overview of the problem, key findings, and strategic recommendations for stakeholders.
- `Research_Paper.md`: Detailed documentation of the methodology and findings supporting the actionable retention initiatives.
- `requirements.txt`: Project dependencies.
- `European_Bank.csv`: (Required) The dataset containing customer banking information. *(Ensure this is placed in the root directory before running the app)*.

## Installation and Usage

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd European_Bank
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

4. **Access the Application:**
   Open your browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Strategic Insights
Our core findings indicate that high balances do not guarantee loyalty (31.2% churn for Inactive High-Balance accounts). Active engagement and optimal product mix (ideally 2 products) drastically reduce churn down to ~7.5%. For more details, see the `Executive_Summary.md` and `Research_Paper.md`.

## Built With
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
