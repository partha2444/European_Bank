import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Retention Analytics", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main theme modifications */
    .css-18e3th9 {
        padding-top: 1.5rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Inter', sans-serif;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
    }
    .metric-title {
        color: #475569;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
    }
    .highlight-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .highlight-card h3 {
        color: white;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv('European_Bank.csv')
    return df

@st.cache_data
def preprocess_data(df):
    median_bal = df[df['Balance'] > 0]['Balance'].median()
    
    def classify_engagement(row):
        if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
            return 'Active Engaged'
        elif row['IsActiveMember'] == 0 and row['Balance'] > median_bal:
            return 'Inactive High-Balance'
        elif row['IsActiveMember'] == 1 and row['NumOfProducts'] == 1:
            return 'Active Low-Product'
        else:
            return 'Inactive Disengaged'
            
    df['EngagementProfile'] = df.apply(classify_engagement, axis=1)
    df['HasCrCard_Label'] = df['HasCrCard'].map({1: 'Yes', 0: 'No'})
    df['IsActive_Label'] = df['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    df['Churn_Label'] = df['Exited'].map({1: 'Churned', 0: 'Retained'})
    return df

try:
    df = load_data()
    df = preprocess_data(df)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=60)
st.sidebar.title("Filters")

geography_filter = st.sidebar.multiselect("Geography", options=df['Geography'].unique(), default=df['Geography'].unique())
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
balance_range = st.sidebar.slider("Balance Threshold", min_value=float(df['Balance'].min()), max_value=float(df['Balance'].max()), value=(float(df['Balance'].min()), float(df['Balance'].max())))
products_filter = st.sidebar.slider("Number of Products", min_value=1, max_value=4, value=(1, 4))

filtered_df = df[
    (df['Geography'].isin(geography_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['Balance'].between(balance_range[0], balance_range[1])) &
    (df['NumOfProducts'].between(products_filter[0], products_filter[1]))
]

# --- MAIN DASHBOARD ---
st.title("Customer Engagement & Retention Analytics")
st.markdown("Analyze behavior patterns to identify strategic retention opportunities, focusing on product utilization rather than pure demographics.")

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
overall_churn = filtered_df['Exited'].mean() * 100
active_churn = filtered_df[filtered_df['IsActiveMember'] == 1]['Exited'].mean() * 100
inactive_churn = filtered_df[filtered_df['IsActiveMember'] == 0]['Exited'].mean() * 100
high_bal_disengaged = filtered_df[filtered_df['EngagementProfile'] == 'Inactive High-Balance']['Exited'].mean() * 100

with col1:
    st.markdown(f'<div class="stMetric"><div class="metric-title">Overall Churn Rate</div><div class="metric-value">{overall_churn:.1f}%</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stMetric"><div class="metric-title">Active Churn Rate</div><div class="metric-value">{active_churn:.1f}%</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stMetric"><div class="metric-title">Inactive Churn Rate</div><div class="metric-value">{inactive_churn:.1f}%</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stMetric"><div class="metric-title">Risk: Premium Inactive Churn</div><div class="metric-value" style="color:#DC2626;">{high_bal_disengaged:.1f}%</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs for Organization
tab1, tab2, tab3 = st.tabs(["Engagement vs Churn", "Product Utilization", "High-Value Detection"])

with tab1:
    st.markdown("""
    <div class="highlight-card">
        <h3>Engagement Retention Ratio Pivot</h3>
        <p>This module investigates the core relationship between activity profiles and customer departure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.5, 1])
    
    with col_a:
        st.subheader("Churn Rate by Engagement Profile")
        profile_churn = filtered_df.groupby('EngagementProfile', as_index=False)['Exited'].mean()
        profile_churn['Exited'] = profile_churn['Exited'] * 100
        fig1 = px.bar(profile_churn, x='EngagementProfile', y='Exited', 
                      color='EngagementProfile', text_auto='.1f',
                      color_discrete_sequence=px.colors.qualitative.Prism,
                      labels={'Exited': 'Churn Rate (%)', 'EngagementProfile': 'Profile'},
                      title="Which Profiles Exhibit Highest Risk?")
        fig1.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, width='stretch')
        
    with col_b:
        st.subheader("Active vs Inactive Cohort Make-up")
        engagement_counts = filtered_df['IsActive_Label'].value_counts().reset_index()
        engagement_counts.columns = ['Status', 'Count']
        fig2 = px.pie(engagement_counts, values='Count', names='Status', hole=0.4,
                      color_discrete_sequence=['#3B82F6', '#94A3B8'])
        st.plotly_chart(fig2, width='stretch')

with tab2:
    st.markdown("### Product Depth Index")
    st.markdown("Examines the influence of possessing single vs. multiple products on customer loyalty.")
    
    prod_churn = filtered_df.groupby('NumOfProducts', as_index=False).agg(
        ChurnRate=('Exited', lambda x: x.mean() * 100),
        CustomerCount=('CustomerId', 'count')
    )
    
    col_prod1, col_prod2 = st.columns(2)
    with col_prod1:
        fig_prod = go.Figure()
        fig_prod.add_trace(go.Bar(
            x=prod_churn['NumOfProducts'],
            y=prod_churn['CustomerCount'],
            name='Total Customers',
            marker_color='#64748B',
            yaxis='y1'
        ))
        fig_prod.add_trace(go.Scatter(
            x=prod_churn['NumOfProducts'],
            y=prod_churn['ChurnRate'],
            name='Churn Rate (%)',
            mode='lines+markers',
            marker=dict(color='#DC2626', size=10),
            line=dict(width=3),
            yaxis='y2'
        ))
        fig_prod.update_layout(
            title="Customer Base vs Churn Rate by Product Count",
            yaxis=dict(title='Total Customers'),
            yaxis2=dict(title='Churn Rate (%)', overlaying='y', side='right', showgrid=False),
            xaxis=dict(title='Number of Products Given', type='category'),
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_prod, width='stretch')
        
    with col_prod2:
        st.subheader("Credit Card Stickiness Score")
        cc_churn = filtered_df.groupby('HasCrCard_Label', as_index=False)['Exited'].mean()
        cc_churn['Exited'] *= 100
        fig_cc = px.bar(cc_churn, x='HasCrCard_Label', y='Exited',
                        text_auto='.1f',
                        color='HasCrCard_Label',
                        color_discrete_sequence=['#0EA5E9', '#F97316'],
                        labels={'Exited': 'Churn Rate (%)', 'HasCrCard_Label': 'Has Credit Card?'},
                        title="Impact of Credit Card Ownership")
        st.plotly_chart(fig_cc, width='stretch')

with tab3:
    st.markdown("""
    <div class="highlight-card" style="background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%);">
        <h3>Premium Disengaged Detection Model</h3>
        <p>Identifying affluent customers who aren't interacting heavily, forming a "silent churn" risk pool.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### High-Balance Disengagement Rate Matrix")
    
    # Let's plot Salary vs Balance mismatch
    fig_scatter = px.scatter(
        filtered_df, x='Balance', y='EstimatedSalary', 
        color='EngagementProfile',
        opacity=0.6,
        hover_data=['Geography', 'Age', 'Exited'],
        color_discrete_map={
            'Active Engaged': '#10B981',
            'Active Low-Product': '#3B82F6',
            'Inactive Disengaged': '#94A3B8',
            'Inactive High-Balance': '#EF4444'
        },
        title="Balance vs Salary Landscape by Engagement"
    )
    st.plotly_chart(fig_scatter, width='stretch')
    
    st.markdown("### At-Risk Premium Cohort Detail")
    at_risk = filtered_df[(filtered_df['EngagementProfile'] == 'Inactive High-Balance') & (filtered_df['Exited'] == 0)]
    st.write(f"Found **{len(at_risk)}** active accounts matching the 'Inactive High-Balance' profile. These require immediate targeted retention efforts.")
    st.dataframe(at_risk[['CustomerId', 'Geography', 'Age', 'Balance', 'EstimatedSalary', 'NumOfProducts']].head(50), width='stretch')

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Unified Mentor • European Central Bank Retention Division Analytics</p>", unsafe_allow_html=True)
