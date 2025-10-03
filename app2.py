import streamlit as st

# --- App Configuration ---
st.set_page_config(
    page_title="Simple Interest Calculator",
    page_icon="💰",
    layout="centered"
)


# --- Main App UI ---
st.title("💰 Simple Interest Calculator")

st.write("This app helps you quickly calculate simple interest and the total amount payable.")

# --- Input Fields ---
st.header("Enter the Details:")

# Using columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "Principal Amount (P)",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        help="The initial amount of money."
    )

with col2:
    time = st.number_input(
        "Time Period in Years (T)",
        min_value=0.0,
        step=0.5,
        format="%.2f",
        help="The duration for which the money is borrowed or invested."
    )

rate = st.number_input(
    "Annual Rate of Interest in % (R)",
    min_value=0.0,
    step=0.1,
    format="%.2f",
    help="The percentage of the principal charged as interest per year."
)


# --- Calculation and Display ---
if st.button("Calculate Interest", type="primary"):
    # Input validation
    if principal > 0 and rate > 0 and time > 0:
        # Calculate simple interest
        simple_interest = (principal * rate * time) / 100

        # Calculate the total amount
        total_amount = principal + simple_interest

        st.header("Calculation Results")
        st.metric(label="Simple Interest", value=f"{simple_interest:,.2f}")
        st.metric(label="Total Amount (Principal + Interest)", value=f"{total_amount:,.2f}")

    else:
        # Show a warning if inputs are not valid
        st.warning("Please make sure all input values are greater than zero.")