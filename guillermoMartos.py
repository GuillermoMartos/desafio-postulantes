from selenium import webdriver
import pandas as pd
import numpy as np
from fastapi import FastAPI


driver=webdriver.Chrome('./chromedriver.exe')

driver.get("https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html")

#cargo los datos del encabezados de la tabla
headers=driver.find_elements_by_tag_name("th")

cols=[]
mylist=[]

#agrego los encabezados de la tabla a lo que serán mis "columnas" del JSON a devolver
for info in headers[0:7]:
    cols.append(info.text)

#ahora voy por los datos de la tabla
tabla=driver.find_elements_by_xpath("//tr/td")

#convierto los webElements de Selenium a texto
for info in tabla:
    mylist.append(info.text)

driver.close()

#acá hago que cada 7 elementos de la lista se componga un arreglo, de tal modo que cada fila de la tabla queda en un mismo y solo arreglo (el número es la cantidad de datos en la tabla total dividido las "columnas")
mylist=np.array_split(mylist, len(mylist)/len(cols))

#unimos tabla y columnas
final=pd.DataFrame(mylist, columns=cols)

#lo jsonizamos dando clave valor por objeto en el arreglo
final=final.to_json(orient = 'records')

print("solución lista en puerto 8000/my-solution")


app = FastAPI()

@app.get("/my-solution")
def hello():
  return {final}