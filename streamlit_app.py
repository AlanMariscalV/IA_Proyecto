import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from apyori import apriori
    
# Estilos CSS para personalizar la barra de navegación

def cargar_datos():
     # Componente para cargar el archivo CSV
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])
    # Verificar si se cargó un archivo
    if uploaded_file is not None:
        # Leer el archivo CSV y cargarlo en un DataFrame
        Lista1 = pd.read_csv(uploaded_file, header = None)
        Transacciones = Lista1.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
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
       # Mostrar el DataFrame
        st.write(Lista1)        
        newList = Lista1.stack().groupby(level=0).apply(list).tolist()
        #newList = Lista1
        return newList
    return("No hay archivo disponible")

def apriori2(data,soporte,elevacion,confianza):
   
    ResultadosC1 = list(apriori(data, 
                   min_support=soporte, 
                   min_confidence=confianza, 
                   min_lift=elevacion))
    Rc1=pd.DataFrame(ResultadosC1)
    for item in ResultadosC1:
        #El primer índice de la lista
        Emparejar = item[0]
        items = [x for x in Emparejar]
        st.write("Regla: " + str(item[0]))
    #El segundo índice de la lista
        st.write("Soporte: " + str(item[1]))
        #El tercer índice de la lista
        st.write("Confianza: " + str(item[2][0][2]))
        st.write("Elevación: " + str(item[2][0][3])) 
        st.write("<----------------------------------------> :)")
def metricas(metrica_seleccionada):
    print("hola")


# Opciones de navegación y contenido de las páginas
pages = {
    "Algoritmo Apriori": "Aqui va teoria",
    "Metricas de distancia": "Aqui va teoria",
    "Clustering": "Aqui va teoria",
    "Ti adoroooooo": "pque"
}

# Mostrar la barra de navegación en la parte superior
selected_page = st.selectbox("", list(pages.keys()), index=0, key="navbar")

# Renderizar la página seleccionada
st.title(selected_page)

if selected_page == "Algoritmo Apriori":
    st.write(pages[selected_page])
    dt = cargar_datos()
    soporte=st.number_input("Ingrese el soporte minimo requerido")
    elevacion=st.number_input("Ingrese la elevacion minima requerido")
    confianza=st.number_input("Ingrese la confianza minima requerido")
    if st.button("Calcular regla"):
       apriori2(dt, soporte, elevacion, confianza)
    
elif selected_page == "Metricas de distancia":
    st.write(pages[selected_page])
    cargar_datos()
    # Casilla de verificación 1
option1 = st.checkbox('Euclidiana')

# Casilla de verificación 2
option2 = st.checkbox('Manhattan')

# Casilla de verificación 3
option3 = st.checkbox('Chevishev')

# Casilla de verificación 4
option4 = st.checkbox('Minkowski')



# Verificar el estado de las casillas de verificación y mostrar mensajes correspondientes
if option1:
    st.write('Opción 1 seleccionada')
if option2:
    st.write('Opción 2 seleccionada')
if option3:
    st.write('Opción 3 seleccionada')

elif selected_page == "Clustering":
    st.write(pages[selected_page])
    cargar_datos()

elif selected_page == "Ti adoroooooo":
    st.write(pages[selected_page])
    cargar_datos()

else:
    st.write(pages[selected_page])

