import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="SpendSense: Global Finance Lab", layout="wide")

EXCHANGE_RATES = {
    "CAD": {"rate": 1.0, "symbol": "$"},
    "INR": {"rate": 69.83, "symbol": "₹"},
    "PKR": {"rate": 202.60, "symbol": "₨"},
    "BDT": {"rate": 89.36, "symbol": "৳"},
    "USD": {"rate": 0.73, "symbol": "$"}
}

def get_financial_quote():
    quotes = [
        "Do not save what is left after spending, but spend what is left after saving.",
        "An investment in knowledge pays the best interest.",
        "Compound interest is the eighth wonder of the world.",
        "Financial freedom is available to those who learn about it and work for it."
    ]
    return random.choice(quotes)

st.sidebar.title("Budget Architect")

selected_currency = st.sidebar.selectbox(
    "Select Your Local Currency:",
    options=list(EXCHANGE_RATES.keys()),
    index=0 # Defaults to CAD
)

currency_info = EXCHANGE_RATES[selected_currency]
rate = currency_info["rate"]
sym = currency_info["symbol"]

income_cad = st.sidebar.number_input("Monthly Net Income (CAD $)", value=3500, step=100)

st.sidebar.write("---")
st.sidebar.subheader("Fixed Expenses (CAD)")
rent = st.sidebar.slider("Housing/Rent", 1000, 3000, 1500)
utilities = st.sidebar.slider("Utilities/Phone", 50, 500, 200)
food = st.sidebar.slider("Groceries", 200, 1000, 500)
transport = st.sidebar.slider("Transport/Fuel", 0, 800, 300)

inflation_rate = st.sidebar.select_slider("2026 Inflation Forecast (%)", options=[0, 2, 5, 10, 15], value=5)

total_expenses_cad = (rent + utilities + food + transport) * (1 + inflation_rate/100)
savings_cad = income_cad - total_expenses_cad

# Convert to Local Currency
total_expenses_local = total_expenses_cad * rate
savings_local = savings_cad * rate

st.title("SpendSense: Global Finance Lab")
st.markdown(f"*{get_financial_quote()}*")
st.write("---")

m1, m2, m3 = st.columns(3)
m1.metric("Total Expenses", f"{sym}{total_expenses_local:,.2f}", delta=f"{inflation_rate}% Inflation", delta_color="inverse")
m2.metric("Monthly Savings", f"{sym}{savings_local:,.2f}")
m3.metric("Savings Rate", f"{(savings_cad/income_cad)*100:.1f}%")

st.write("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"Expense Breakdown ({selected_currency})")
    df_pie = pd.DataFrame({
        "Category": ["Housing", "Utilities", "Groceries", "Transport"],
        "Amount": [rent * rate, utilities * rate, food * rate, transport * rate]
    })
    fig = px.pie(df_pie, values='Amount', names='Category', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader(f"5-Year Investment ({selected_currency})")
    return_rate = st.slider("Estimated Return Rate (%)", 1, 12, 7)
    
    # Compound interest for 5 years
    future_value_local = savings_local * (((1 + (return_rate/100/12))**(12*5) - 1) / (return_rate/100/12))
    
    st.info(f"Investing {sym}{savings_local:,.0f} monthly at {return_rate}% growth:")
    st.title(f"{sym}{future_value_local:,.2f}")

st.write("---")
st.caption(f"SpendSense v1.4 | Exchange Rates updated for May 21, 2026 | Location: Calgary")
