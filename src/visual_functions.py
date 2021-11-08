import pandas as pd
import ast

def ordenadito(city,d0,d1,d2):
    """
    Argumentos: 3 listas
    Recibe 1 str y 3 listas y me forma un dataframe ordenadito.
    edit: me estaba cogiendo las listas como string, las reconvierto a lista
    """
    d0 = ast.literal_eval(d0)
    d1 = ast.literal_eval(d1)
    d2 = ast.literal_eval(d2)
        
    diccio = {city : ["T_max", "t_min", "prob_lluvia", "tiempo", "icono"],
                "d0" : d0,
                "d1" : d1,
                "d2" : d2}

    return pd.DataFrame(diccio)
    

from PIL import Image
import requests
from io import BytesIO

def dibujar(tit):
    """
    dibuja una imagen a partir de un titulo
    """
    url = f"http:{tit}"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

import matplotlib.pyplot as plt

def dibu3(data):
    """
    dibuja los 3 iconos en linea correspondientes a los 3 dias de un dataframe
    """
    fig = plt.figure(figsize=(5, 5))
    
    for i in range(1,4):
        image=dibujar(data.T[4][i])
        fig.add_subplot(1, 3, i)
        plt.imshow(image)
        plt.axis('off')