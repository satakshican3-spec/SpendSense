import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import date

REGIONAL_PROFILES = {
    "Canada (CAD)": {"rate": 1.0, "sym": "$", "income": 4500, "rent": 1800, "util": 250, "food": 600, "trans": 400},
    "India (INR)": {"rate": 69.83, "sym": "₹", "income": 75000, "rent": 22000, "util": 5000, "food": 15000, "trans": 6000},
    "Pakistan (PKR)": {"rate": 202.49, "sym": "₨", "income": 150000, "rent": 40000, "util": 18000, "food": 35000, "trans": 12000},
    "Bangladesh (BDT)": {"rate": 89.36, "sym": "৳", "income": 65000, "rent": 18000, "util": 6000, "food": 18000, "trans": 5000},
    "USA (USD)": {"rate": 0.73, "sym": "$", "income": 4200, "rent": 1700, "util": 350, "food": 550, "trans": 550}
}

st.set_page_config(page_title="SpendSense Global", layout="wide")

def get_daily_wisdom():
    quotes = [
        "Do not save what is left after spending, but spend what is left after saving.",
        "An investment in knowledge pays the best interest.",
        "Compound interest is the eighth wonder of the world.",
        "Financial freedom is available to those who learn about it and work for it.",
        "Beware of little expenses; a small leak will sink a great ship."
    ]
    return random.choice(quotes)

st.sidebar.title("Economic Architect")
st.sidebar.caption("Localized Budget Strategy")

region = st.sidebar.selectbox("Active Economic Profile", options=list(REGIONAL_PROFILES.keys()))
profile = REGIONAL_PROFILES[region]
sym = profile["sym"]

st.sidebar.write("---")
income = st.sidebar.number_input(f"Monthly Net Income ({sym})", value=float(profile["income"]), step=500.0)

st.sidebar.subheader("Expense Vectors")
rent = st.sidebar.number_input(f"Housing & Rent ({sym})", value=float(profile["rent"]), step=100.0)
util = st.sidebar.number_input(f"Utilities & Digital ({sym})", value=float(profile["util"]), step=50.0)
food = st.sidebar.number_input(f"Food & Groceries ({sym})", value=float(profile["food"]), step=50.0)
trans = st.sidebar.number_input(f"Transportation ({sym})", value=float(profile["trans"]), step=50.0)

st.sidebar.write("---")
inflation = st.sidebar.select_slider("2026 Inflation Impact (%)", options=list(range(0, 16)), value=5)

total_base = rent + util + food + trans
total_adjusted = total_base * (1 + inflation/100)
monthly_savings = income - total_adjusted
savings_rate = (monthly_savings / income * 100) if income > 0 else 0

st.title(f"SpendSense: {region} Intelligence")
st.markdown(f"*{get_daily_wisdom()}*")
st.write("---")

k1, k2, k3 = st.columns(3)
k1.metric("Total Expenses", f"{sym}{total_adjusted:,.0f}", delta=f"{inflation}% Inflation", delta_color="inverse")
k2.metric("Monthly Savings", f"{sym}{monthly_savings:,.0f}")
k3.metric("Savings Rate", f"{savings_rate:.1f}%")

st.write("---")

col_viz, col_invest = st.columns(2)

with col_viz:
    st.subheader("Expense Distribution Matrix")
    df_pie = pd.DataFrame({
        "Category": ["Housing", "Utilities", "Food", "Transport"],
        "Amount": [rent, util, food, trans]
    })
    fig = px.pie(df_pie, values='Amount', names='Category', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col_invest:
    st.subheader("5-Year Capital Growth Simulation")
    return_rate = st.slider("Projected Annual Return (%)", 1, 15, 8)
    
    if monthly_savings > 0:
        # Future value of a monthly annuity
        fv = monthly_savings * (((1 + (return_rate/100/12))**(12*5) - 1) / (return_rate/100/12))
        st.info(f"Investing {sym}{monthly_savings:,.0f}/mo at {return_rate}% yields:")
        st.title(f"{sym}{fv:,.0f}")
    else:
        st.warning("Increase monthly savings to unlock investment projections.")

st.write("---")
st.caption(f"SpendSense v1.7 | Economic Environment: May 21, 2026 | Currency: {sym} ({region})")
