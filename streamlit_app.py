import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

    
# Estilos CSS para personalizar la barra de navegación

def cargar_datos():
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

    



# Opciones de navegación y contenido de las páginas
pages = {
    "Algoritmo Apriori": "Aqui va teoria",
    "Metricas de distancia ": "Aqui va teoria",
    "Clustering": "Aqui va teoria",
    "Ti adoroooooo": "pque"
}

# Mostrar la barra de navegación en la parte superior
selected_page = st.selectbox("", list(pages.keys()), index=0, key="navbar")

# Renderizar la página seleccionada
st.title(selected_page)

if selected_page == "Algoritmo Apriori":
    st.write(pages[selected_page])
    cargar_datos()

elif selected_page == "Metricas de distancia":
    st.write(pages[selected_page])
    cargar_datos()

elif selected_page == "Clustering":
    st.write(pages[selected_page])
    cargar_datos()

elif selected_page == "Ti adoroooooo":
    st.write(pages[selected_page])
    cargar_datos()
    

else:
    st.write(pages[selected_page])

