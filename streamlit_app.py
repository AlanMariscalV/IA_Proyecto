import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

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
  
    plt.figure(figsize=(16,20), dpi=300)
    plt.ylabel('Item')
    plt.xlabel('Frecuencia')
    plt.barh(Lista['Item'], width=Lista['Frecuencia'], color='red')
    grafica_path = 'grafica.png'
    image = plt.savefig(grafica_path)
    st.image("grafica.png", caption="Carga pofavo", use_column_width=True)