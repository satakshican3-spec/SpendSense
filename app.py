import streamlit as st

st.set_page_config(page_title="Spendsense Budgeter", layout="wide")

st.title("Spendsense: Global Budget Simulator")
st.write("Calculate your 2026 living costs and savings potential in Canada.")

profile = st.selectbox("Select your life situation", ["Single Person", "Student", "International Student", "Family"])

gender = ""
family_size = 0

if profile in ["Single Person", "Student", "International Student"]:
    gender = st.radio("Select Gender", ["Boy", "Girl"])
else:
    family_size = st.slider("How many people are in your family?", 2, 8, 4)

income = st.number_input("Total Monthly Income (CAD)", min_value=0, value=4000)

st.write("---")

if profile == "Family":
    default_rent = 2500 + (family_size * 250)
    default_food = family_size * 350
    default_ins = 300 + (family_size *50)
elif profile == "International Student":
    default_rent = 1200
    default_food = 500
    default_ins = 100
else:
    default_rent = 1800
    default_food = 600
    default_ins = 150

col1, col2 = st.columns(2)

with col1:
    rent = st.number_input("Housing and Utilities", value=default_rent)
    groceries = st.number_input("Groceries and Essentials", value=default_food)
    insurance = st.number_input("Insurance (Health/Auto/Tenant)", value=default_ins)

with col2:
    transport = st.number_input('Transportation", value=150)
    household = st.number_input("Household Items/Misc", value=150)

    extra_costs = 0
    if profile == "International Student":
        st.info("Requirement: $22,895/year proof of funds needed.")
        tuition = st.number_input("Monthly Tuition Portion", value=2500)
        extra_costs = tuition
    elif profile == "Family":
        st.info(f"Budgeting for a family of {family_size}.")
        childcare = st.number_input("Childcare/Education Fees", value=500 * (family_size // 3))
        extra_costs = childcare

total_expenses = rent + groceries + insurance + transport + household + extra_costs
savings = income - total_expenses

st.write("---")
st.subheader("Monthly Financial Summary")

c1, c2, c3 = st.columns(3)
c1.metric("Total Expenses", f"${total_expenses}")
c2.metric("Monthly Savings", f"${savings}")
c3.metric("Yearly Projection", f"${savings * 12}")

if savings < 0:
    st.error("Warning: Your expenses are higher than your income.")
else:
    st.success(f"Great! As a {profile} ({gender if gender else family_size}), you have a healthy savings rate.")
