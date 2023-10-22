import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Upload file",
    page_icon="open_file_folder",
    )

st.sidebar.title("Upload data")
st.sidebar.subheader("Provide and manage files with custom data")
status_tag = st.sidebar.markdown("___status___: Choose a file")

def update_status(status_message):
    status_tag.markdown(f"___status___: {status_message}")

if st.session_state.uploaded_arrays:
    num_files = len(st.session_state.uploaded_arrays)
    num_files_str = f"{num_files} file{'s' if num_files > 1 else ''}"
    update_status(f"Uploaded {num_files_str}")

st.title("Upload data")
st.text("Here you can upload your own files to analyze them later")

st.session_state.warnings = False

def parse_file(file):
    lines = file.readlines()
    if len(lines) > 1:
        st.warning(
            "File contains more than one line",
            icon="⚠️")
        st.session_state.warnings = True
    return np.array([float(x) for x in lines[0].split()])

if "uploaded_arrays" not in st.session_state:
    st.session_state.uploaded_arrays = {}

uploaded_file = st.file_uploader("Upload here")
if uploaded_file is not None:
    try:
        array = parse_file(uploaded_file)
        st.write("Parsed content", array[np.newaxis, :])
        if uploaded_file.name in st.session_state.uploaded_arrays:
            st.warning(
            "File with the same name already exsisted and was overriden",
            icon="⚠️")
            st.session_state.warnings = True
        st.session_state.uploaded_arrays[uploaded_file.name] = array
        if st.session_state.warnings:
            update_status("Uploaded with warnings")
        else:
            update_status("Successfully uploaded")
    except ValueError:
        st.error(
            "File is not a space-separated list of floats",
            icon="❗")
        update_status("Error while uploading")
