import streamlit as st
import numpy as np
from backbones import backbone_dict

st.set_page_config(
    page_title="Demo App",
    page_icon="bar_chart",
    menu_items={
        "About": "Demonstrational app made with Streamlit"
    })

st.title("Mean value calculator")

column_data, column_computation = st.columns(2)

with column_data:
    array_size = st.slider("Number of values", 
        min_value=1,
        max_value=15,
        value=5
    )
    st.write("List of random values:")
    array = np.random.randint(1, 10, size=array_size)
    st.write(array[np.newaxis, :])
    st.button("Regenerate values")

with column_computation:
    backbone_name = st.selectbox("Backbone: ",
        backbone_dict.keys())
    engine_instance = backbone_dict[backbone_name]()

st.divider()

if st.button("Get mean value"):
    with st.spinner():
        mean = engine_instance.calculate(array)
    st.write("**Result:**", mean)
