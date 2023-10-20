import streamlit as st
import numpy as np
import timeit
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
    array = np.random.randint(1, 10, size=array_size)
    if 'saved_array' in st.session_state:
        saved_size = st.session_state.saved_array.size
        array[:saved_size] = st.session_state.saved_array[:array_size] 
    st.session_state.saved_array = array
    st.write("List of random values:")
    st.write(array[np.newaxis, :])
    if st.button("Regenerate values"):
        del st.session_state['saved_array']
        st.rerun()

with column_computation:
    backbone_name = st.selectbox("Backbone: ",
        backbone_dict.keys())
    engine_instance = backbone_dict[backbone_name]()
    timing_on = st.checkbox("Measure perfomance")

st.divider()

if st.button("Get mean value"):
    time_start = timeit.default_timer() if timing_on else 0
    with st.spinner("Calculating..."):
        mean = engine_instance.calculate(array)
    time_end = timeit.default_timer() if timing_on else 0
    total_time_ms = round((time_end - time_start) * 1000)
    result_message = f"**Result:**```{mean:.2f}```"
    if timing_on:
        result_message += f"_(```{total_time_ms}ms```elapsed)_"
    st.write(result_message)
