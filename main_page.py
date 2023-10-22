import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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
st.header("Set up engine and data")

column_data, column_computation = st.columns(2)

with column_data:
    array_size, array = None, None
    chosen_array = "Randomized"
    if st.session_state.get("uploaded_arrays"):
        chosen_array = st.selectbox(
            "Chose data to analyze",
            ["Randomized"] + list(st.session_state.uploaded_arrays.keys()))
    if chosen_array == "Randomized":
        array_size = st.slider("Number of values", 
            min_value=1,
            max_value=15,
            value=5,
        )
        array = np.random.randint(1, 10, size=array_size)
        if 'saved_array' in st.session_state:
            saved_size = st.session_state.saved_array.size
            array[:saved_size] = st.session_state.saved_array[:array_size] 
        st.session_state.saved_array = array
    else:
        array = st.session_state.uploaded_arrays[chosen_array]
        array_size = array.size
    st.write("List of random values:"
        if chosen_array == "Randomized"
        else "Uploaded file content")
    st.write(array[np.newaxis, :])
    if chosen_array == "Randomized":
        if st.button("Regenerate values"):
            del st.session_state.saved_arrays['saved_array']
            st.rerun()

with column_computation:
    backbone_name = st.selectbox("Backbone: ",
        backbone_dict.keys())
    engine_instance = backbone_dict[backbone_name]()
    timing_on = st.checkbox("Measure perfomance")

st.header("Calculate result")

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

st.header("Explore data")

with st.expander(
    label="Data visualization",
    expanded=bool(st.session_state.get('keep_maximized')),
    ):
    sns.set()
    fig = plt.figure()
    ax = sns.histplot(array, discrete=True)
    ax.set(xlabel='Values')
    ax.set_xticks(np.arange(1, 10))
    st.pyplot(fig, dpi=200)

    keep_maximized = st.checkbox(
        label="Keep maximized _(experimental)_",
        key="keep_maximized")
