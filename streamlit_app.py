import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
    
# Estilos CSS para personalizar la barra de navegación
css = """
<style>
    .navbar {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f5f5f5;
        padding: 10px;
        margin-bottom: 20px;
    }
    .navbar-item {
        margin: 0 10px;
    }
</style>
"""

# Aplicar los estilos CSS
st.markdown(css, unsafe_allow_html=True)

# Opciones de navegación y contenido de las páginas
pages = {
    "Inicio": "¡Bienvenido a la página de inicio!",
    "Página 1": "Este es el contenido de la página 1.",
    "Página 2": "Aquí tienes el contenido de la página 2.",
    "Página 3": "Este es el contenido de la página 3."
}

# Mostrar la barra de navegación en la parte superior
selected_page = st.selectbox("", list(pages.keys()), index=0, key="navbar")

# Renderizar la página seleccionada
st.title(selected_page)

if selected_page == "Inicio":
    st.write(pages[selected_page])

elif selected_page == "Página 1":
    st.write(pages[selected_page])
    # Título de la página
    st.title("Carga de archivo CSV en Streamlit")

    # Componente para cargar el archivo CSV
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

    # Verificar si se cargó un archivo
    if uploaded_file is not None:
        # Leer el archivo CSV y cargarlo en un DataFrame
        df = pd.read_csv(uploaded_file)

        # Mostrar el DataFrame
        st.write(df)
        
        Transacciones = df.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
        Lista = pd.DataFrame(Transacciones)
        Lista['Frecuencia'] = 1
        Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
        Lista = Lista.rename(columns={0 : 'Item'})
    
        fig=plt.figure(figsize=(16,20), dpi=300)
        plt.ylabel('Item')
        plt.xlabel('Frecuencia')
        plt.barh(Lista['Item'], width=Lista['Frecuencia'], color='red')
        st.pyplot(fig)

else:
    st.write(pages[selected_page])