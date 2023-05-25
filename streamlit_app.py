import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from apyori import apriori
from scipy.spatial.distance import cdist 
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from kneed import KneeLocator
    

#__________________________________________________ FUNCION CARGAR DATOS_________________________________________________________________________

def cargar_datos(seleccion):
     # Componente para cargar el archivo CSV
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])
    # Verificar si se cargó un archivo
    if uploaded_file is not None:
        # Leer el archivo CSV y cargarlo en un DataFrame
        #para apriori
        if seleccion == 0:
          Lista1 = pd.read_csv(uploaded_file, header = None)
        #para metricas
        elif seleccion == 1:
            Lista1 = pd.read_csv(uploaded_file)
        Transacciones = Lista1.values.reshape(-1).tolist() #-1 significa 'dimensión no conocida'
        Lista = pd.DataFrame(Transacciones)
        Lista['Frecuencia'] = 1
        Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
        Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
        Lista = Lista.rename(columns={0 : 'Item'})
        
       # Mostrar el DataFrame
        st.write(Lista1)        
        newList = Lista1.stack().groupby(level=0).apply(list).tolist()
        #newList = Lista1
        return newList,Lista1,Lista
    return("No hay archivo disponible")

#__________________________________________________ FUNCION MOSTRAR GRAFICA_________________________________________________________________________


def mostrar_grafica(lista):
    fig=plt.figure(figsize=(16,20), dpi=300)
    plt.ylabel('Item')
    plt.xlabel('Frecuencia')
    plt.barh(lista['Item'], width=lista['Frecuencia'], color='red')
    st.pyplot(fig)

#__________________________________________________ FUNCION APRIORI_________________________________________________________________________

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

#__________________________________________________ FUNCION METRICAS________________________________________________________________________

def metricas(dato,metrica_seleccionada,lambda1 = 0):
    estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler o MinMaxScaler 
    MEstandarizada = estandarizar.fit_transform(dato)
    estandarizadapd = pd.DataFrame(MEstandarizada)
    if metrica_seleccionada == 'minkowski':
       Dst = cdist(estandarizadapd[0:10], estandarizadapd[0:10], metric=metrica_seleccionada, p=lambda1)
    else:
        Dst = cdist(estandarizadapd[0:10], estandarizadapd[0:10], metric=metrica_seleccionada)
    Matriz = pd.DataFrame(Dst)
    st.write(Matriz.round(3))
    return Matriz
    
#__________________________________________________ FUNCION DISTANCIA_________________________________________________________________________

def sacarDistancia(metrica,MEstandarizada,lambda2 = 0):
        options = ['0','1', '2', '3','4', '5', '6','7', '8', '9']
        selected_options = st.multiselect('Selecciona dos objetos para sacar la distancia:', options)
        if st.button("Enviar dato"):
            if len(selected_options) == 2:
                o=[]
                for elecciones in selected_options:
                    o.append(int(elecciones))
                Objeto1 = MEstandarizada[o[0]]
                Objeto2 = MEstandarizada[o[1]]
                if metrica == 1: 
                    dst = distance.euclidean(Objeto1,Objeto2)
                elif metrica == 2: 
                    dst = distance.cityblock(Objeto1,Objeto2)
                elif metrica == 3: 
                    dst = distance.chebyshev(Objeto1,Objeto2)
                elif metrica == 4: 
                    dst = distance.minkowski(Objeto1,Objeto2,lambda2)
                st.write("La distancia entre los objetos es: ", dst)
            elif len(selected_options) > 2:
                st.write('¡Has seleccionado más de dos opciones! Selecciona solo dos.')
            else:
                st.write('Selecciona dos opciones.')


def ACD(data):
    Correlacion=data.corr(method='pearson')
    figura=plt.figure(figsize=(14,7))
    MatrizInf = np.triu(Correlacion)
    sns.heatmap(Correlacion, cmap='RdBu_r', annot=True, mask=MatrizInf)
    st.write(figura)
    options=[]
   # for i in range(0,len(data[0])):
    #    options.append(i)
    #st.write(len(data.columns))
    df=pd.DataFrame(data)
    nombres_columnas=df.columns
    st.write(nombres_columnas)
    options = [nombres_columnas[a] for a in range(2, len(data.columns))]
    selected_options = st.multiselect('Selecciona los indices de las variables que quieras trabajar', options)
    if st.checkbox("Enviar dato"):
        MatrizVariables=np.array(data[selected_options])
        st.write(MatrizVariables)
        estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler o MinMaxScaler 
        MEstandarizada = estandarizar.fit_transform(MatrizVariables)   # Se calculan la media y desviación y se escalan los datos
        pd_estandarizado=pd.DataFrame(MEstandarizada)
        return pd_estandarizado
    
def Cluster_Jerarquico(data_frame,csv):
    figura= plt.figure(figsize=(10, 7))
    plt.title("Pacientes con cáncer de mama")
    plt.xlabel('Observaciones')
    plt.ylabel('Distancia')
    Arbol = shc.dendrogram(shc.linkage(data_frame, method='complete', metric='euclidean'))
    st.write(figura)
    numero = st.number_input("Ingrese el numero de clusters", step=1, value=0, format="%d")
    MJerarquico = AgglomerativeClustering(n_cluster=numero, linkage='complete', affinity='euclidean')
    MJerarquico.fit_predict(data_frame)
    csv['clusterH'] = MJerarquico.labels_
    st.write(csv)
   

    #plt.axhline(y=5.4, color='orange', linestyle='--')
    #Probar con otras mediciones de distancia (chebyshev, cityblock)
    

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

#__________________________________________________ APRIORI_________________________________________________________________________
if selected_page == "Algoritmo Apriori":
    st.write(pages[selected_page])
    dt = cargar_datos(0)
    mostrar_grafica(dt[2])
    soporte=st.number_input("Ingrese el soporte minimo requerido")
    elevacion=st.number_input("Ingrese la elevacion minima requerido")
    confianza=st.number_input("Ingrese la confianza minima requerido")
    if st.button("Calcular regla"):
       apriori2(dt[0], soporte, elevacion, confianza)

#__________________________________________________ metricas_distancia_________________________________________________________________________

    
elif selected_page == "Metricas de distancia":
    st.write(pages[selected_page])
    dato=cargar_datos(1)
    options = ['Métrica Euclidiana', 'Métrica Manhattan', 'Métrica Chevishev', 'Métrica Minkowski']
    selected_option = st.radio('Selecciona una opción:', options)
  
   
# Verificar el estado de las casillas de verificación y mostrar mensajes correspondientes
    Matriz=[0]
    if selected_option == 'Métrica Euclidiana':
        st.write('Opción 1 seleccionada')
        opcion = 1
        Matriz=metricas(dato[1], 'euclidean')
        sacarDistancia(opcion,Matriz)
    if selected_option == 'Métrica Manhattan':
        st.write('Opción 2 seleccionada')
        opcion = 2
        Matriz=metricas(dato[1],'cityblock')
        sacarDistancia(opcion,Matriz)
    if selected_option == 'Métrica Chevishev':
        st.write('Opción 3 seleccionada')
        opcion = 3
        Matriz=metricas(dato[1],'chebyshev')
        sacarDistancia(opcion,Matriz)
    if selected_option == 'Métrica Minkowski':
        st.write('Opción 4 seleccionada')
        opcion = 4
        input_lambda = st.number_input("Ingresa el valor de lambda: ")
        if st.checkbox("Obtener matriz"): 
            Matriz=metricas(dato[1],'minkowski',lambda1= input_lambda)
            
        sacarDistancia(opcion,Matriz,lambda2=input_lambda)
        print("hola mivida")

    
#__________________________________________________ CLUSTERING_________________________________________________________________________
    
#HOLA MI AMOR <3
elif selected_page == "Clustering":
    st.write(pages[selected_page])
    dato=cargar_datos(1)
    dt=ACD(dato[1])
    Cluster_Jerarquico(dt,dato[1])
    

    #st.write(dato[1])


elif selected_page == "Ti adoroooooo":
    st.write(pages[selected_page])
    cargar_datos()

else:
    st.write(pages[selected_page])











