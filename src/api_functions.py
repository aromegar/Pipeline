import json
import requests

from amadeus import Client, ResponseError

import os
from dotenv import load_dotenv

load_dotenv()

mykey = os.getenv("weatherapi")
Amad_k = os.getenv("Ama_key")
Amad_s = os.getenv("Ama_secret")


def Amad(orig,destin,date):
    """
    Argumentos: orig = un str de 3 letras (el código IATA del aeropuerto de origen)
                destin = un str de 3 letras (el código IATA del aeropuerto de destino)
                date = un str en formato yyyy-mm-dd con la fecha de vuelo
    Devuelve una LISTA con información del vuelo
    """
    try:
        amadeus = Client(client_id=f"{Amad_k}",client_secret=f"{Amad_s}")

        resp = amadeus.shopping.flight_offers_search.get(
            originLocationCode=f"{orig}",
            destinationLocationCode=f"{destin}",
            departureDate=f"{date}",
            adults=1)
        
        return resp.data
    except: 
        return "no flights"


def W_fc3(coor):
    """
    Argumento: una tupla de 2 floats con 4 decimales cada uno.
    Recibe una tupla y llama a la API de Weather con parámetros mi key y las coordenadas de la tupla.
    Devuelve la parte que me interesa del json, para LOS PRÓXIMOS 3 DÍAS.
    """
    parametros={"key":f"{mykey}", "q":coor, "days":3}
    resp = requests.get("http://api.weatherapi.com/v1/forecast.json", params=parametros).json()
    return resp["forecast"]["forecastday"]