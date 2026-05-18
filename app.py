import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="SpendSense: 2026 Finance Lab", layout="wide")

def get_financial_quote():
    quotes = [
        "Do not save what is left after spending, but spend what is left after saving.",
        "Beware of little expenses; a small leak will sink a great ship.",
        "An investment in knowledge pays the best interest.",
        "Compound interest is the eighth wonder of the world.",
        "Financial freedom is available to those who learn about it and work for it."
    ]
    return random.choice(quotes)

st.sidebar.title("Budget Architect")
income = st.sidebar.number_input("Monthly Net Income ($)", value=3500, step=100)

st.sidebar.write("---")
st.sidebar.subheader("Fixed Expenses")
rent = st.sidebar.slider("Housing/Rent", 1000, 3000, 1500)
utilities = st.sidebar.slider("Utilities", 50, 500, 200)
food = st.sidebar.slider("Groceries", 200, 1000, 500)
transport = st.sidebar.slider("Transport/Fuel", 0, 800, 300)

st.sidebar.write("---")
inflation_rate = st.sidebar.select_slider("2026 Inflation Forecast (%)", options=[0, 2, 5, 8, 10, 15], value=5)

total_expenses = (rent + utilities + food + transport) * (1 + inflation_rate/100)
savings = income - total_expenses

st.title("SpendSense: Financial Simulation Lab")
st.markdown(f"*{get_financial_quote()}*")
st.write("---")

m1, m2, m3 = st.columns(3)
m1.metric("Total Expenses", f"${total_expenses:,.2f}", delta=f"{inflation_rate}% Inflation", delta_color="inverse")
m2.metric("Monthly Savings", f"${savings:,.2f}")
m3.metric("Savings Rate", f"{(savings/income)*100:.1f}%")

st.write("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Expense Distribution")
    df_pie = pd.DataFrame({
        "Category": ["Housing", "Utilities", "Groceries", "Transport"],
        "Amount": [rent, utilities, food, transport]
    })
    fig = px.pie(df_pie, values='Amount', names='Category', hole=0.4,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Investment 'What-If' (5 Year Growth)")
    rate = st.slider("Estimated Return Rate (%)", 1, 12, 7)
    future_value = savings *(((1 + (rate/100/12))**(12*5) - 1) / (rate/100/12))
    st.info(f"If you invest your **${savings:,.0f}** savings at **{rate}%**, in 5 years you'll have:")
    st.title(f"${future_value:,.2f}")

st.write("---")
st.caption("SpendSense v1.3 | Calgary Economic Asset | No Data Tracking")
