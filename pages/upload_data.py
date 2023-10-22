import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Upload file",
    page_icon="open_file_folder",
    )

st.title("Upload data")
st.text("Here you can upload your own files to analyze them later")

def parse_file(file):
    lines = file.readlines()
    if len(lines) > 1:
        st.warning(
            "File contains more than one line",
            icon="⚠️")
    return np.array([float(x) for x in lines[0].split()])

if "uploaded_arrays" not in st.session_state:
    st.session_state.uploaded_arrays = {}

uploaded_file = st.file_uploader("Upload here")
if uploaded_file is not None:
    try:
        array = parse_file(uploaded_file)
        st.write("Parsed content", array[np.newaxis, :])
        st.session_state.uploaded_arrays[uploaded_file.name] = array
    except ValueError:
        st.error(
            "File is not a space-separated list of floats",
            icon="❗")
