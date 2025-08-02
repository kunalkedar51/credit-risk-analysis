import plotly.graph_objects as go
import plotly.express as px

def create_metrics_gauge(value, title, max_value=100):
    """Create a gauge chart for metrics visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value/3], 'color': "lightgreen"},
                {'range': [max_value/3, 2*max_value/3], 'color': "yellow"},
                {'range': [2*max_value/3, max_value], 'color': "red"}
            ]
        }
    ))
    fig.update_layout(height=200)
    return fig

def create_financial_summary(metrics, monthly_income):
    """Create a pie chart for financial summary"""
    labels = ['Monthly Loan Payment', 'Other Expenses', 'Available Income']
    values = [
        metrics['monthly_payment'],
        monthly_income * (metrics['expense_ratio']/100/12),
        monthly_income - (metrics['monthly_payment'] + monthly_income * (metrics['expense_ratio']/100/12))
    ]
    
    fig = px.pie(
        values=values,
        names=labels,
        title='Monthly Financial Breakdown'
    )
    return fig

def get_risk_color(risk_level):
    """Get color based on risk level"""
    colors = {
        "Low": "green",
        "Medium": "yellow",
        "High": "red"
    }
    return colors.get(risk_level, "gray")