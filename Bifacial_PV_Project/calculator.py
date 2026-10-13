import streamlit as st

st.title("Simple Calculator")

# Input number
number1 = st.number_input("Enter first number")

number2 = st.number_input("Enter second number")

# Select operation
operation = st.selectbox(
    "Choose operation",
    ["Addition (+)", "Multiplication (×)", "Division (÷)"]
)

# Calculate
if st.button("Calculate"):

    if operation == "Addition (+)":
        result = number1 + number2

    elif operation == "Multiplication (×)":
        result = number1 * number2

    elif operation == "Division (÷)":
        if number2 != 0:
            result = number1 / number2
        else:
            st.error("Cannot divide by zero!")
            result = None

    if result is not None:
        st.success(f"Answer = {result}")