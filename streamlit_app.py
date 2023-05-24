import streamlit as st
import pandas as pd
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
        Lista1.drop([0], axis=0,inplace=True)
        Lista1.drop([0], axis=1,inplace=True)
        # Mostrar el DataFrame
        st.write(Lista1)        
        Transacciones = Lista1.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
        Lista1.stack().groupby(level=0).apply(list).tolist()
        newList = Lista1

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
        return newList
    return("No hay archivo disponible")

def apriori2(data,soporte,elevacion,confianza):
    ReglasC1 = apriori(data, 
                   min_support=soporte, 
                   min_confidence=confianza, 
                   min_lift=elevacion)
    #ResultadosC1 = list(ReglasC1)
    #Rc1=pd.DataFrame(ResultadosC1)
    #for item in ResultadosC1:
        #El primer índice de la lista
        #Emparejar = item[0]
        #items = [x for x in Emparejar]
        #st.write("Regla: " + str(item[0]))
    #El segundo índice de la lista
        #st.write("Soporte: " + str(item[1]))
        #El tercer índice de la lista
        #st.write("Confianza: " + str(item[2][0][2]))
        #st.write("Elevación: " + str(item[2][0][3])) 
    st.write(ReglasC1 + "=====================================") # Aquí deberíamos asociar el valor correspondiente a la etiqueta


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

elif selected_page == "Clustering":
    st.write(pages[selected_page])
    cargar_datos()

elif selected_page == "Ti adoroooooo":
    st.write(pages[selected_page])
    cargar_datos()

else:
    st.write(pages[selected_page])

