# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 08:36:20 2019

@author: lserpa
"""
import numpy as np
import pandas as pd

#1. Cargar en el entorno el "poblacionMunicipios.csv"
df_poblac_municipios = pd.read_csv('poblacionMunicipios.csv')
df_poblac_municipios.set_index(df_poblac_municipios.CodProvincia, inplace = True)
df_poblac_municipios.index.name = None
#2. Elimina las filas correspondientes a municipios sin población
df_poblac_municipios = df_poblac_municipios[df_poblac_municipios.Poblacion > 0]
#3. Imprime el total de la poblacion de todos los municipios
total_pob = sum(df_poblac_municipios.Poblacion)
#4. Crea un DataFrame de Pandas donde la primera columna sean las provincias, la segunda el numero de habitantes por provincia, tercera la desviación típica en el numero de habitantes por provincia y la cuarta el numero de municipios por provincia
prov = pd.DataFrame(df_poblac_municipios.drop_duplicates(['Provincia']).iloc[:,1])
pob_mun = []
num_municipios = []
desviacion_tipica = []
for x in range(1,len(prov)+1):
    try:
        pob = sum(df_poblac_municipios.loc[x,['Provincia', 'Poblacion']].Poblacion)
        num_mun = len(df_poblac_municipios.loc[x,['Provincia', 'CodMunicipio', 'Poblacion']].CodMunicipio)
        desv_tip = np.std(df_poblac_municipios.loc[x,['Provincia', 'Poblacion']].Poblacion)
    except:
        pob = int(df_poblac_municipios.loc[x,['Poblacion']])
        num_mun = 1
    pob_mun.append(pob)
    num_municipios.append(num_mun)
    desviacion_tipica.append(desv_tip)
prov['Habitantes por provincia'] = pob_mun
prov['Desv. Típica'] = desviacion_tipica
prov['Num. de Municipios'] = num_municipios
#5. Cargar el archivo "CP_Municipios.csv"
df_CP_municipios = pd.read_csv('CP_Municipios.csv')
df_CP_municipios.set_index(df_CP_municipios.CodProvincia, inplace = True)
df_CP_municipios.index.name = None
#6. Empleando el código de provincia y de municipio, cruza los dos datasets. El resultado debe ser un DataFrame
df_Merge = df_CP_municipios.merge(df_poblac_municipios, on = ['CodMunicipio','CodProvincia'])
#7. Generar un CSV llamado "faltan.csv" que debe estar vacío
df_Vacio = df_CP_municipios.merge(df_poblac_municipios, on = ['Municipio'])
df_Vacio = df_Vacio[df_Vacio.CP == np.nan]
df_Vacio.to_csv('faltan.csv', header = False)
#8. Agrupa la información por código postal. Se quiere un DataFrame con las siguientes columnas
cod_post = pd.DataFrame(df_Merge.drop_duplicates(['CP']).loc[:,'CP'])
numero_municipios = []
poblacion_CP = []
provincia_CP = []
for x in cod_post.CP:
    try:
        n_munic = len(df_Merge.loc[df_Merge['CP'] == x].Municipio_x)
        cp_pob = sum(df_Merge.loc[df_Merge['CP'] == x].Poblacion)
        cp_prov = df_Merge.loc[df_Merge['CP'] == x].drop_duplicates(['Provincia']).Provincia.iloc[-1]
    except:
        n_munic = 1
        cp_pob = df_Merge.loc[df_Merge['CP'] == x].Poblacion
    numero_municipios.append(n_munic)
    poblacion_CP.append(cp_pob)
    provincia_CP.append(cp_prov)
cod_post['Numero de municipios'] = numero_municipios
cod_post['Población por CP'] = poblacion_CP
cod_post['Provincia del CP'] = provincia_CP
#    * Código postal
#    * Numero de municipios que tienen dicho código postal asignado
#    * Población: se calculará como la suma de la población de todos los municipios que incluyen dicho código postal
#    * Provincia a la que está asignado el código postal