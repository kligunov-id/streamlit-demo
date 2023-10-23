import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Upload file",
    page_icon="open_file_folder",
    )

uploaded_files_limit = 5

class EmptyFileError(Exception):
    pass

st.sidebar.title("Upload data")
st.sidebar.subheader("Provide and manage files with custom data")
status_tag = st.sidebar.markdown("___status___: Choose a file")

def update_status(status_message):
    status_tag.markdown(f"___status___: {status_message}")

if st.session_state.get("uploaded_arrays"):
    num_files = len(st.session_state.uploaded_arrays)
    num_files_str = f"{num_files} file{'s' if num_files > 1 else ''}"
    update_status(f"Uploaded {num_files_str}")

st.title("Upload data")
st.markdown("Here you can upload your own files to analyze them later")

st.session_state.warnings = 0
st.session_state.errors = 0

def warning(message):
    st.warning(message, icon="⚠️")
    st.session_state.warnings += 1

def error(message):
    st.error(message, icon="❗")
    st.session_state.errors += 1

def parse_file(file):
    lines = file.readlines()
    if len(lines) > 1:
        warning("File contains more than one line")
    return np.array([float(x) for x in lines[0].split()])

if "uploaded_arrays" not in st.session_state:
    st.session_state.uploaded_arrays = {}

if len(st.session_state.uploaded_arrays) < uploaded_files_limit:
    uploaded_file = st.file_uploader("Upload here")
    if uploaded_file is not None:
        try:
            array = parse_file(uploaded_file)
            if array.size == 0:
                raise EmptyFileError()
            st.write("Parsed content", array[np.newaxis, :])
            if uploaded_file.name in st.session_state.uploaded_arrays:
                warning("File with the same name already exsisted and was overriden")
            st.session_state.uploaded_arrays[uploaded_file.name] = array
        except ValueError:
            error("File is not a space-separated list of floats")
        except EmptyFileError:
            error("File is empty")
        else:
            if st.session_state.warnings:
                update_status("Uploaded with warnings")
            else:
                update_status("Successfully uploaded")
        if st.session_state.errors:
            update_status("Error while uploading")
else:
    st.markdown(f"You have reached the upload limit of {uploaded_files_limit} files. To upload new data, first delete some")

if st.session_state.uploaded_arrays:
    st.markdown("Previously uploaded:")
    for array_name in st.session_state.uploaded_arrays:
        name_column, array_column, button_column = st.columns([.2, .65, .15])
        name_column.markdown(array_name)
        array_column.write(
            st.session_state.uploaded_arrays[array_name][np.newaxis,:])
        def delete_array():
            del st.session_state.uploaded_arrays[array_name]
        button_column.button("Delete",
            on_click=delete_array,
            key=array_name)

