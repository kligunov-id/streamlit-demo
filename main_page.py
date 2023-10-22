import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import timeit
import math
from backbones import (
    backbone_dict,
    parse_options,
    TwoMuchTokensError,
    NotHyphenatedOptionError)

st.set_page_config(
    page_title="Demo App",
    page_icon="bar_chart",
    menu_items={
        "About": "Demonstrational app made with Streamlit"
    })

st.sidebar.title("Main page")
st.sidebar.subheader("Set up engine and prepare data")
status_tag = st.sidebar.markdown("___status___: Ready")

def update_status(status_message):
    status_tag.markdown(f"___status___: {status_message}")

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
            del st.session_state['saved_array']
            st.rerun()

def try_parsing_options(options_line, engine_cls):
    try:
        parsed_options = parse_options(options_line, engine_cls)
        return parsed_options
    except ValueError:
        st.error(
            "Parameter value is not an integer",
            icon="❗")
    except TwoMuchTokensError:
        st.error(
            "Option is described by more than two tokens",
            icon="❗")
    except NotHyphenatedOptionError:
        st.error("The first option is not hyphenated",
            icon="❗")
    return None

with column_computation:
    backbone_name = st.selectbox("Backbone: ",
        backbone_dict.keys())
    options_line = st.text_input("Engine options:")
    st.markdown("Examples of options line:")
    st.markdown("```-squared -error``` for variance calculation")
    st.markdown("```-sleep 1``` with slow engine to regulate speed")
    parsed_options = try_parsing_options(
        options_line,
        engine_cls=backbone_dict[backbone_name])
    flags, parameters = None, None
    if parsed_options is None:
        update_status("Error while parsing options")
    else:
        flags, parameters, unrecognized_flags, unrecognized_parameters = parsed_options
        if unrecognized_flags or unrecognized_parameters:
            update_status("Some options not recognized")
        if unrecognized_flags:
            st.warning(
                f"Not recognized flag{'s' if len(unrecognized_flags) > 1 else ''} {', '.join(unrecognized_flags)}",
                icon="⚠️")
        if unrecognized_parameters:
            st.warning(
                f"Not recognized parameter{'s' if len(unrecognized_parameters) > 1 else ''} {', '.join(unrecognized_parameters.keys())}",
                icon="⚠️")
    engine_instance = backbone_dict[backbone_name](flags, parameters)
    timing_on = st.checkbox("Measure perfomance")

st.header("Calculate result")

if st.button("Get mean value"):
    update_status("Processing...")
    time_start = timeit.default_timer() if timing_on else 0
    with st.spinner("Calculating..."):
        mean = engine_instance.calculate(array)
    time_end = timeit.default_timer() if timing_on else 0
    update_status("Finished")
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
    max_xtick = math.ceil(array.max()) + 1
    min_xtick = math.floor(array.min())
    small_discrete = max_xtick - min_xtick < 15
    ax = sns.histplot(array, discrete=small_discrete)
    ax.set(xlabel='Values')
    ax.set_xticks(np.arange(
            math.floor(array.min()),
            math.ceil(array.max()) + 1))
    st.pyplot(fig, dpi=200)

    keep_maximized = st.checkbox(
        label="Keep maximized _(experimental)_",
        key="keep_maximized")
