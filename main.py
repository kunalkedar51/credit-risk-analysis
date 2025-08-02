import streamlit as st
import pandas as pd
from utils import load_data, calculate_risk_metrics, determine_risk_level
from risk_analyzer import create_metrics_gauge, create_financial_summary, get_risk_color

# Page configuration
st.set_page_config(
    page_title="Loan Risk Analysis System",
    page_icon="💰",
    layout="wide"
)

# Load data
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()

# Title and description
st.title("Loan Risk Analysis System")
st.markdown("""
This system analyzes loan applications based on financial metrics and provides 
risk assessment and recommendations for loan approval.
""")

# Input form
st.subheader("Loan Application Form")
with st.form("loan_application"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.selectbox("Applicant Name", options=sorted(df['Name'].unique()))
    
    with col2:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=1000,
            max_value=1000000,
            value=50000,
            step=1000
        )
    
    with col3:
        loan_tenure = st.number_input(
            "Loan Tenure (months)",
            min_value=12,
            max_value=360,
            value=60,
            step=12
        )
    
    submitted = st.form_submit_button("Analyze Application")

if submitted:
    # Get applicant data
    applicant_data = df[df['Name'] == name]
    
    if len(applicant_data) == 0:
        st.error("Applicant not found in database!")
    else:
        # Calculate metrics
        metrics = calculate_risk_metrics(applicant_data, loan_amount, loan_tenure)
        risk_level = determine_risk_level(metrics)
        
        # Display risk level
        st.subheader("Risk Assessment")
        risk_color = get_risk_color(risk_level)
        st.markdown(
            f'<div style="padding:10px;border-radius:5px;background-color:{risk_color};'
            f'color:black;text-align:center;font-size:24px">Risk Level: {risk_level}</div>',
            unsafe_allow_html=True
        )
        
        # Loan recommendation
        st.subheader("Loan Recommendation")
        if risk_level == "High":
            st.error("❌ Loan application not recommended for approval")
        else:
            st.success("✅ Loan application recommended for approval")
        
        # Display metrics
        st.subheader("Financial Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            # DTI Ratio gauge
            st.plotly_chart(
                create_metrics_gauge(
                    metrics['dti_ratio'],
                    "Debt-to-Income Ratio (%)",
                    100
                ),
                use_container_width=True
            )
            
            # Savings Ratio gauge
            st.plotly_chart(
                create_metrics_gauge(
                    metrics['savings_ratio'],
                    "Savings Ratio (%)",
                    100
                ),
                use_container_width=True
            )
        
        with col2:
            # Financial breakdown
            st.plotly_chart(
                create_financial_summary(
                    metrics,
                    applicant_data['Monthly_Income'].iloc[0]
                ),
                use_container_width=True
            )
        
        # Display detailed metrics
        st.subheader("Detailed Financial Information")
        metrics_df = pd.DataFrame({
            'Metric': [
                'Monthly Income ($)',
                'Monthly Loan Payment ($)',
                'Yearly Savings ($)',
                'Total Expenses ($)'
            ],
            'Value': [
                f"{applicant_data['Monthly_Income'].iloc[0]:,.2f}",
                f"{metrics['monthly_payment']:,.2f}",
                f"{applicant_data['Yearly_Savings'].iloc[0]:,.2f}",
                f"{applicant_data['Total_Expenses'].iloc[0]:,.2f}"
            ]
        })
        st.table(metrics_df)

# Add footer
st.markdown("""
---
### How Risk Assessment Works
- **Low Risk**: Excellent financial health with good debt-to-income ratio and savings
- **Medium Risk**: Acceptable financial metrics but with some concerns
- **High Risk**: Significant risk factors present in the application
""")
