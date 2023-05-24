import streamlit as st
st.title("intento imagen")

uploaded_file=st.file_uploader("selecciona",type=["jpg","jpeg","png"])

if uploaded_file is not None:

    st.image(uploaded_file,caption="imagen cargada",use_colum_width=True)
