import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

# Variable de estado para realizar el seguimiento de la página actual
current_page = st.sidebar.radio("Navegación", ["Inicio", "Página 1", "Página 2", "Página 3"])

# Renderizar la página actual en función de la selección
if current_page == "Inicio":
    st.title("Página de Inicio")
    # Contenido de la página de inicio
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

elif current_page == "Página 1":
    st.title("Página 1")
    # Contenido de la página 1

elif current_page == "Página 2":
    st.title("Página 2")
