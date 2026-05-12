import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from ml_engine import train_model, predict_risk_scores

# ─── PAGE CONFIG ───
st.set_page_config(page_title="Retention Analytics Pro", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# ─── CUSTOM CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
h1, h2, h3 { color: #1E3A8A; }
.kpi-card {
    background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
    padding: 18px; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #3B82F6; text-align: center;
}
.kpi-card .label { color: #64748B; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card .value { font-size: 1.8rem; font-weight: 700; color: #0F172A; margin: 4px 0 0; }
.kpi-card.red { border-left-color: #DC2626; }
.kpi-card.green { border-left-color: #10B981; }
.kpi-card.amber { border-left-color: #F59E0B; }
.highlight-card {
    background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
    color: white; padding: 20px; border-radius: 12px; margin-bottom: 16px;
}
.highlight-card h3 { color: white; margin-top: 0; }
.highlight-card.red { background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%); }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ───
@st.cache_data
def load_data():
    df = pd.read_csv('European_Bank.csv')
    return df

@st.cache_data
def preprocess_data(df):
    median_bal = df[df['Balance'] > 0]['Balance'].median()
    def classify(row):
        if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
            return 'Active Engaged'
        elif row['IsActiveMember'] == 0 and row['Balance'] > median_bal:
            return 'Inactive High-Balance'
        elif row['IsActiveMember'] == 1 and row['NumOfProducts'] == 1:
            return 'Active Low-Product'
        else:
            return 'Inactive Disengaged'
    df['EngagementProfile'] = df.apply(classify, axis=1)
    df['HasCrCard_Label'] = df['HasCrCard'].map({1: 'Yes', 0: 'No'})
    df['IsActive_Label'] = df['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    df['Churn_Label'] = df['Exited'].map({1: 'Churned', 0: 'Retained'})
    df['AgeBand'] = pd.cut(df['Age'], bins=[0,25,35,45,55,65,100],
                           labels=['18-25','26-35','36-45','46-55','56-65','65+'])
    df['CreditBand'] = pd.cut(df['CreditScore'], bins=[299,500,600,700,800,851],
                              labels=['300-500','501-600','601-700','701-800','801-850'])
    df['TenureBand'] = pd.cut(df['Tenure'], bins=[-1,2,5,7,10],
                              labels=['0-2yr','3-5yr','6-7yr','8-10yr'])
    df['RSI'] = ((df['Tenure']/10)*30 + (df['NumOfProducts']/4)*40 +
                 df['IsActiveMember']*30).round(1)
    avg_bal = df[df['Balance']>0]['Balance'].mean()
    df['CLV_Est'] = ((df['Balance']/avg_bal) * df['RSI'] * (1 + df['Tenure']/10)).round(0)
    return df

@st.cache_resource
def get_ml_results(df_raw):
    return train_model(df_raw, model_type='random_forest')

try:
    raw_df = load_data()
    df = preprocess_data(raw_df.copy())
    ml = get_ml_results(raw_df)
    df = predict_risk_scores(df, ml['model'], ml['feature_cols'])
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# ─── SIDEBAR ───
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=55)
st.sidebar.title("🔍 Filters")
geo = st.sidebar.multiselect("Geography", df['Geography'].unique(), default=list(df['Geography'].unique()))
gen = st.sidebar.multiselect("Gender", df['Gender'].unique(), default=list(df['Gender'].unique()))
bal = st.sidebar.slider("Balance Range", float(df['Balance'].min()), float(df['Balance'].max()),
                        (float(df['Balance'].min()), float(df['Balance'].max())))
prods = st.sidebar.slider("Products", 1, 4, (1, 4))
age = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()),
                         (int(df['Age'].min()), int(df['Age'].max())))
tenure = st.sidebar.slider("Tenure (years)", 0, 10, (0, 10))
risk_tiers = st.sidebar.multiselect("Risk Tier", ['Low','Medium','High','Critical'],
                                    default=['Low','Medium','High','Critical'])

fdf = df[
    (df['Geography'].isin(geo)) & (df['Gender'].isin(gen)) &
    (df['Balance'].between(bal[0], bal[1])) &
    (df['NumOfProducts'].between(prods[0], prods[1])) &
    (df['Age'].between(age[0], age[1])) &
    (df['Tenure'].between(tenure[0], tenure[1])) &
    (df['RiskTier'].isin(risk_tiers))
]

# ─── HEADER ───
st.title("🏦 Customer Engagement & Retention Analytics Pro")
st.caption("Behavior-driven retention strategy with predictive ML churn forecasting")

# ─── TOP KPIs ───
c1, c2, c3, c4, c5, c6 = st.columns(6)
churn_rate = fdf['Exited'].mean()*100 if len(fdf) else 0
active_churn = fdf[fdf['IsActiveMember']==1]['Exited'].mean()*100 if len(fdf[fdf['IsActiveMember']==1]) else 0
inactive_churn = fdf[fdf['IsActiveMember']==0]['Exited'].mean()*100 if len(fdf[fdf['IsActiveMember']==0]) else 0
ihb = fdf[fdf['EngagementProfile']=='Inactive High-Balance']
ihb_churn = ihb['Exited'].mean()*100 if len(ihb) else 0
rev_at_risk = fdf[fdf['ChurnProbability']>=50]['Balance'].sum()
avg_rsi = fdf['RSI'].mean() if len(fdf) else 0

def kpi(col, label, val, css=""):
    col.markdown(f'<div class="kpi-card {css}"><div class="label">{label}</div><div class="value">{val}</div></div>', unsafe_allow_html=True)

kpi(c1, "Overall Churn", f"{churn_rate:.1f}%")
kpi(c2, "Active Churn", f"{active_churn:.1f}%", "green")
kpi(c3, "Inactive Churn", f"{inactive_churn:.1f}%", "amber")
kpi(c4, "Premium Inactive", f"{ihb_churn:.1f}%", "red")
kpi(c5, "Revenue at Risk", f"€{rev_at_risk:,.0f}", "red")
kpi(c6, "Avg RSI Score", f"{avg_rsi:.1f}/100", "green")

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ───
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Engagement vs Churn", "📦 Product Utilization",
    "🎯 High-Value Detection", "🤖 ML Predictions",
    "🔬 Segmentation Deep-Dive", "📥 Reports"
])

# ═══════════════════════ TAB 1 ═══════════════════════
with tab1:
    st.markdown("""<div class="highlight-card"><h3>Engagement Retention Ratio Pivot</h3>
    <p>Core relationship between activity profiles and customer departure.</p></div>""", unsafe_allow_html=True)
    ca, cb = st.columns([1.5, 1])
    with ca:
        pc = fdf.groupby('EngagementProfile', as_index=False)['Exited'].mean()
        pc['Exited'] *= 100
        fig = px.bar(pc, x='EngagementProfile', y='Exited', color='EngagementProfile',
                     text_auto='.1f', color_discrete_sequence=px.colors.qualitative.Prism,
                     labels={'Exited':'Churn Rate (%)','EngagementProfile':'Profile'},
                     title="Churn Rate by Engagement Profile")
        fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with cb:
        ec = fdf['IsActive_Label'].value_counts().reset_index()
        ec.columns = ['Status','Count']
        fig2 = px.pie(ec, values='Count', names='Status', hole=0.45,
                      color_discrete_sequence=['#3B82F6','#94A3B8'])
        fig2.update_layout(title="Active vs Inactive Split")
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════ TAB 2 ═══════════════════════
with tab2:
    st.markdown("### Product Depth Index")
    pch = fdf.groupby('NumOfProducts', as_index=False).agg(
        ChurnRate=('Exited', lambda x: x.mean()*100), Count=('CustomerId','count'))
    cp1, cp2 = st.columns(2)
    with cp1:
        figp = go.Figure()
        figp.add_trace(go.Bar(x=pch['NumOfProducts'], y=pch['Count'], name='Customers', marker_color='#64748B'))
        figp.add_trace(go.Scatter(x=pch['NumOfProducts'], y=pch['ChurnRate'], name='Churn %',
                                  mode='lines+markers', marker=dict(color='#DC2626',size=10),
                                  line=dict(width=3), yaxis='y2'))
        figp.update_layout(title="Customer Base vs Churn by Product Count",
                           yaxis=dict(title='Customers'), yaxis2=dict(title='Churn %', overlaying='y', side='right'),
                           xaxis=dict(title='Products', type='category'),
                           plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.01,y=0.99))
        st.plotly_chart(figp, use_container_width=True)
    with cp2:
        cc = fdf.groupby('HasCrCard_Label', as_index=False)['Exited'].mean()
        cc['Exited'] *= 100
        figcc = px.bar(cc, x='HasCrCard_Label', y='Exited', text_auto='.1f',
                       color='HasCrCard_Label', color_discrete_sequence=['#0EA5E9','#F97316'],
                       labels={'Exited':'Churn %','HasCrCard_Label':'Credit Card?'},
                       title="Credit Card Stickiness")
        st.plotly_chart(figcc, use_container_width=True)

# ═══════════════════════ TAB 3 ═══════════════════════
with tab3:
    st.markdown("""<div class="highlight-card red"><h3>Premium Disengaged Detection</h3>
    <p>Affluent customers with low interaction — the "silent churn" risk pool.</p></div>""", unsafe_allow_html=True)
    figs = px.scatter(fdf, x='Balance', y='EstimatedSalary', color='EngagementProfile', opacity=0.6,
                      hover_data=['Geography','Age','Exited','ChurnProbability'],
                      color_discrete_map={'Active Engaged':'#10B981','Active Low-Product':'#3B82F6',
                                          'Inactive Disengaged':'#94A3B8','Inactive High-Balance':'#EF4444'},
                      title="Balance vs Salary by Engagement Profile")
    st.plotly_chart(figs, use_container_width=True)
    at_risk = fdf[(fdf['EngagementProfile']=='Inactive High-Balance') & (fdf['Exited']==0)]
    st.metric("At-Risk Premium Accounts", len(at_risk), delta=f"€{at_risk['Balance'].sum():,.0f} in balances")
    st.dataframe(at_risk[['CustomerId','Geography','Age','Balance','EstimatedSalary',
                          'NumOfProducts','ChurnProbability','RiskTier','RSI']].sort_values(
                              'ChurnProbability', ascending=False).head(50), use_container_width=True)

# ═══════════════════════ TAB 4: ML ═══════════════════════
with tab4:
    st.markdown("""<div class="highlight-card"><h3>🤖 Predictive Churn Model</h3>
    <p>Random Forest classifier trained on 80/20 split with stratified sampling.</p></div>""", unsafe_allow_html=True)

    # Metrics row
    m = ml['metrics']
    mc1,mc2,mc3,mc4,mc5 = st.columns(5)
    mc1.metric("Accuracy", f"{m['accuracy']:.3f}")
    mc2.metric("Precision", f"{m['precision']:.3f}")
    mc3.metric("Recall", f"{m['recall']:.3f}")
    mc4.metric("F1-Score", f"{m['f1']:.3f}")
    mc5.metric("ROC-AUC", f"{m['roc_auc']:.3f}")

    rc1, rc2 = st.columns(2)
    with rc1:
        st.subheader("ROC Curve")
        roc_fig = go.Figure()
        roc_fig.add_trace(go.Scatter(x=ml['fpr'], y=ml['tpr'], mode='lines',
                                     name=f"AUC={m['roc_auc']:.3f}", line=dict(color='#3B82F6',width=3)))
        roc_fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
                                     name='Random', line=dict(dash='dash',color='#94A3B8')))
        roc_fig.update_layout(xaxis_title='FPR', yaxis_title='TPR', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(roc_fig, use_container_width=True)
    with rc2:
        st.subheader("Confusion Matrix")
        cm = ml['confusion_matrix']
        cm_fig = px.imshow(cm, text_auto=True, labels=dict(x="Predicted",y="Actual"),
                           x=['Retained','Churned'], y=['Retained','Churned'],
                           color_continuous_scale='Blues')
        st.plotly_chart(cm_fig, use_container_width=True)

    st.subheader("Feature Importance")
    fi = ml['feature_importances']
    fig_fi = px.bar(fi, x='Importance', y='Feature', orientation='h',
                    color='Importance', color_continuous_scale='Viridis',
                    title="What Drives Churn?")
    fig_fi.update_layout(yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_fi, use_container_width=True)

    st.subheader("Risk Distribution")
    rd1, rd2 = st.columns(2)
    with rd1:
        risk_counts = fdf['RiskTier'].value_counts().reset_index()
        risk_counts.columns = ['Tier','Count']
        fig_rt = px.pie(risk_counts, values='Count', names='Tier', hole=0.45,
                        color='Tier', color_discrete_map={
                            'Low':'#10B981','Medium':'#F59E0B','High':'#F97316','Critical':'#DC2626'})
        fig_rt.update_layout(title="Customer Risk Tier Distribution")
        st.plotly_chart(fig_rt, use_container_width=True)
    with rd2:
        fig_hist = px.histogram(fdf, x='ChurnProbability', nbins=30,
                                color_discrete_sequence=['#3B82F6'],
                                title="Churn Probability Distribution")
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)

# ═══════════════════════ TAB 5: SEGMENTATION ═══════════════════════
with tab5:
    st.markdown("### 🔬 Customer Segmentation Deep-Dive")
    s1, s2 = st.columns(2)
    with s1:
        age_churn = fdf.groupby('AgeBand', as_index=False).agg(
            ChurnRate=('Exited', lambda x: x.mean()*100), Count=('CustomerId','count'))
        fig_age = px.bar(age_churn, x='AgeBand', y='ChurnRate', text_auto='.1f',
                         color='ChurnRate', color_continuous_scale='OrRd',
                         title="Churn Rate by Age Band")
        fig_age.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_age, use_container_width=True)
    with s2:
        geo_eng = fdf.groupby(['Geography','EngagementProfile'], as_index=False)['Exited'].mean()
        geo_eng['Exited'] *= 100
        fig_ge = px.bar(geo_eng, x='Geography', y='Exited', color='EngagementProfile',
                        barmode='group', text_auto='.1f', title="Geography × Engagement Churn",
                        color_discrete_sequence=px.colors.qualitative.Set2)
        fig_ge.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ge, use_container_width=True)

    s3, s4 = st.columns(2)
    with s3:
        ten_churn = fdf.groupby('TenureBand', as_index=False).agg(
            ChurnRate=('Exited', lambda x: x.mean()*100), AvgRSI=('RSI','mean'))
        fig_ten = px.bar(ten_churn, x='TenureBand', y='ChurnRate', text_auto='.1f',
                         color='AvgRSI', color_continuous_scale='Viridis',
                         title="Churn by Tenure Cohort (color=RSI)")
        fig_ten.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ten, use_container_width=True)
    with s4:
        gen_prod = fdf.groupby(['Gender','NumOfProducts'], as_index=False)['Exited'].mean()
        gen_prod['Exited'] *= 100
        fig_gp = px.bar(gen_prod, x='NumOfProducts', y='Exited', color='Gender',
                        barmode='group', text_auto='.1f', title="Gender × Product Churn",
                        color_discrete_sequence=['#8B5CF6','#EC4899'])
        fig_gp.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(type='category'))
        st.plotly_chart(fig_gp, use_container_width=True)

    st.subheader("Credit Score Risk Heatmap")
    heat = fdf.groupby(['CreditBand','EngagementProfile'], as_index=False)['Exited'].mean()
    heat['Exited'] *= 100
    heat_pivot = heat.pivot(index='CreditBand', columns='EngagementProfile', values='Exited')
    fig_heat = px.imshow(heat_pivot, text_auto='.1f', color_continuous_scale='RdYlGn_r',
                         title="Churn % — Credit Score Band vs Engagement Profile",
                         labels=dict(color="Churn %"))
    st.plotly_chart(fig_heat, use_container_width=True)

# ═══════════════════════ TAB 6: REPORTS ═══════════════════════
with tab6:
    st.markdown("### 📥 Downloadable Reports")
    st.markdown("Export filtered data, at-risk customers, and ML predictions.")

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("**Filtered Data (CSV)**")
        csv1 = fdf.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download Filtered Data", csv1, "filtered_data.csv", "text/csv")
    with r2:
        st.markdown("**At-Risk Customers (CSV)**")
        risk_df = fdf[fdf['ChurnProbability'] >= 50].sort_values('ChurnProbability', ascending=False)
        csv2 = risk_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download At-Risk Report", csv2, "at_risk_customers.csv", "text/csv")
    with r3:
        st.markdown("**ML Predictions Full (CSV)**")
        pred_cols = ['CustomerId','Surname','Geography','Gender','Age','Balance',
                     'NumOfProducts','IsActiveMember','EngagementProfile',
                     'ChurnProbability','RiskTier','RSI','CLV_Est']
        csv3 = fdf[pred_cols].to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download Predictions", csv3, "ml_predictions.csv", "text/csv")

    st.markdown("---")
    st.subheader("📄 Executive Summary Report (PDF)")
    try:
        from fpdf import FPDF
        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 18)
            pdf.cell(0, 12, "Retention Analytics - Executive Report", ln=True, align="C")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, f"Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
            pdf.ln(8)

            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Key Performance Indicators", ln=True)
            pdf.set_font("Helvetica", "", 11)
            for label, val in [("Overall Churn Rate", f"{churn_rate:.1f}%"),
                               ("Active Member Churn", f"{active_churn:.1f}%"),
                               ("Inactive Member Churn", f"{inactive_churn:.1f}%"),
                               ("Premium Inactive Churn", f"{ihb_churn:.1f}%"),
                               ("Revenue at Risk", f"EUR {rev_at_risk:,.0f}"),
                               ("Average RSI", f"{avg_rsi:.1f}/100")]:
                pdf.cell(0, 7, f"  {label}: {val}", ln=True)
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "ML Model Performance", ln=True)
            pdf.set_font("Helvetica", "", 11)
            for k, v in ml['metrics'].items():
                pdf.cell(0, 7, f"  {k.title()}: {v:.3f}", ln=True)
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Risk Tier Distribution", ln=True)
            pdf.set_font("Helvetica", "", 11)
            for tier in ['Critical','High','Medium','Low']:
                cnt = len(fdf[fdf['RiskTier']==tier])
                pdf.cell(0, 7, f"  {tier}: {cnt} customers ({cnt/len(fdf)*100:.1f}%)", ln=True)
            pdf.ln(5)

            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 10, "Top Feature Importances", ln=True)
            pdf.set_font("Helvetica", "", 11)
            for _, row in ml['feature_importances'].head(5).iterrows():
                pdf.cell(0, 7, f"  {row['Feature']}: {row['Importance']:.4f}", ln=True)

            return bytes(pdf.output())

        pdf_bytes = generate_pdf()
        st.download_button("⬇ Download PDF Report", pdf_bytes, "executive_report.pdf", "application/pdf")
    except ImportError:
        st.info("Install `fpdf2` for PDF export: pip install fpdf2")

# ─── FOOTER ───
st.markdown("---")
st.markdown("<p style='text-align:center;color:#64748B;'>Unified Mentor • European Central Bank Retention Division Analytics • ML-Powered</p>", unsafe_allow_html=True)
