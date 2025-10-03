import streamlit as st
import pandas as pd
import numpy as np

# set title of the app
st.title("My First Streamlit App")

# display a markdown-formatted header
st.header("This is a header")

# display static text
st.write("this is a simple streamlit app.")

# display a button
if st.button("Click Me"):
    st.balloons()
    st.write("Button clicked!")

# input widget example
number = st.slider('Select a number', 0, 100, 25) # 'label', min, max, default
st.write(f'You selected: {number}')

# data display
df = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['feature_A', 'feature_B']
)
st.subheader("Random Datan Preview")
st.dataframe(df)  # interactive table