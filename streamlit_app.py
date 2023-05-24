import streamlit as st

# Título de la página
st.title("Carga de imágenes en Streamlit")

# Componente para cargar la imagen
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

# Verificar si se cargó un archivo
if uploaded_file is not None:
    # Mostrar la imagen cargada
    st.image(uploaded_file, caption="Imagen cargada", use_column_width=True)