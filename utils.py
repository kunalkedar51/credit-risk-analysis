import pandas as pd
import numpy as np

def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv("C:\\Users\\kedar\\Desktop\\mini project\\individual_expense_dataset_50_unique_names.csv")
    return df

def calculate_risk_metrics(applicant_data, loan_amount, loan_tenure):
    """Calculate risk metrics for loan application"""
    monthly_income = applicant_data['Monthly_Income'].iloc[0]
    yearly_savings = applicant_data['Yearly_Savings'].iloc[0]
    total_expenses = applicant_data['Total_Expenses'].iloc[0]
    
    # Calculate monthly loan payment (simple calculation)
    monthly_interest = applicant_data['Interest_Rate'].iloc[0] / 1200  # Convert annual rate to monthly
    monthly_payment = (loan_amount * monthly_interest * (1 + monthly_interest)**loan_tenure) / ((1 + monthly_interest)**loan_tenure - 1)
    
    # Calculate debt-to-income ratio
    dti_ratio = (monthly_payment / monthly_income) * 100
    
    # Calculate savings ratio
    savings_ratio = (yearly_savings / (monthly_income * 12)) * 100
    
    # Calculate expense ratio
    expense_ratio = (total_expenses / (monthly_income * 12)) * 100
    
    return {
        'monthly_payment': monthly_payment,
        'dti_ratio': dti_ratio,
        'savings_ratio': savings_ratio,
        'expense_ratio': expense_ratio
    }

def determine_risk_level(metrics):
    """Determine risk level based on calculated metrics"""
    dti_ratio = metrics['dti_ratio']
    savings_ratio = metrics['savings_ratio']
    expense_ratio = metrics['expense_ratio']
    
    # Risk scoring system
    risk_score = 0
    
    # DTI ratio evaluation
    if dti_ratio > 43:
        risk_score += 3
    elif dti_ratio > 36:
        risk_score += 2
    elif dti_ratio > 28:
        risk_score += 1
        
    # Savings ratio evaluation
    if savings_ratio < 10:
        risk_score += 3
    elif savings_ratio < 20:
        risk_score += 2
    elif savings_ratio < 30:
        risk_score += 1
        
    # Expense ratio evaluation
    if expense_ratio > 80:
        risk_score += 3
    elif expense_ratio > 60:
        risk_score += 2
    elif expense_ratio > 40:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 7:
        return "High"
    elif risk_score >= 4:
        return "Medium"
    else:
        return "Low"
