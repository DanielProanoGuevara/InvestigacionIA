# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:25:19 2019

@author: lserpa
"""

archivo = open("FicheroALeer.txt")
lectura = archivo.read()
archivo.close()

#Contar numero de líneas
def num_lineas(texto):
     resultado = texto.splitlines()
     return(len(resultado))
     

#Número de ocurrencias de palaba "el"
ocurrencias_el = lectura.count(" el ")
ocurrencias_El = lectura.count(" El ")
total_ocurrencias = ocurrencias_el + ocurrencias_El

#eliminar tildes y hacer minusculas
def normalizar(texto):
    #hacer todas minúsculas
    texto = texto.lower()
    
    #tupla de reemplazos
    reemplazos = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            )
    for inic, fin in reemplazos:
        texto = texto.replace(inic, fin)
    return texto

text = normalizar(lectura)

#crear archivo de texto
try:
    nuevo = open("resultado.txt", "x")
except:
    nuevo = open("resultado.txt", "w")

nuevo.write(str(num_lineas(lectura)))
nuevo.write("\n"+str(total_ocurrencias))
nuevo.write("\n"+text)
nuevo.close()
