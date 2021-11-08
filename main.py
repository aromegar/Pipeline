### importamos librerías:

import pandas as pd
import datetime

from src import dataset_functions as ds
from src import api_functions as af


## importamos el dataframe y lo limpiamos un poco:

df = pd.read_csv("DATA/airports.dat")

headers = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "latitude", "longitude", "altitude", "Time Zone", "DST", "tzdatabase time zone", "Type", "Source"]
head_mal = list(df.columns)
dic_head = { head_mal[i]: headers[i] for i in range(len(head_mal))}
df.rename(columns = dic_head, inplace=True)
df.drop(["Airport ID", "ICAO", "Time Zone", "DST", "tzdatabase time zone", "Type", "Source","altitude"], axis=1, inplace=True)

### vamos a quedarnos sólo con los 20 aeropuertos más grandes de Europa, y limpiamos un poco más:

lista20=["LHR","CDG","AMS","FRA","BER","BCN","LGW","MUC","FCO","BRU","VIE","MXP","DUB","ZRH","CPH","PRG","MAN","OSL","LIS","ARN"]
df=df[df.IATA.isin(lista20)]
df["coord"]=df.apply(lambda fila: ds.coordenadas(fila.latitude,fila.longitude), axis=1)
df.drop(["Name","latitude","longitude"], axis=1, inplace=True)


## obtenemos los precios con la API de Amadeus:

today = datetime.date.today()
d1 = today.strftime("%Y-%m-%d")
pasm = today + datetime.timedelta(days=2)
d2 = pasm.strftime("%Y-%m-%d")

## le pido los precios de ida con mi función af.Amad:

df["resp_ida"]=df["IATA"].apply(lambda iata : af.Amad("MAD",iata,d1))

df["precio_ida"]=df.apply(lambda fila : fila.resp_ida[0]["price"]["total"], axis=1)
df["comp_ida"]=df.apply(lambda fila : fila.resp_ida[0]["validatingAirlineCodes"][0], axis=1)

### y los de vuelta, 2 días más tarde:

df["resp_vuelta"]=df["IATA"].apply(lambda iata : af.Amad(iata,"MAD",d2))

df["precio_vuelta"]=df.apply(lambda fila : fila.resp_vuelta[0]["price"]["total"], axis=1)
df["comp_vuelta"]=df.apply(lambda fila : fila.resp_vuelta[0]["validatingAirlineCodes"][0], axis=1)

### y recolocamos columnas:

df.drop(["resp_ida","resp_vuelta"], axis=1, inplace=True)

df["precio_ida"] = df["precio_ida"].astype(dtype="float64")
df["precio_vuelta"] = df["precio_vuelta"].astype(dtype="float64")
df["precio_total"] = df["precio_ida"]+df["precio_vuelta"]


## ahora vamos a sacar los datos meteorológicos de la API de weatherapi.com

df["datos"] = df["coord"].apply(af.W_fc3)

df["day0"]=df.apply(lambda fila : [fila["datos"][0]["day"]["maxtemp_c"],
                                   fila["datos"][0]["day"]["mintemp_c"],
                                   fila["datos"][0]["day"]["daily_chance_of_rain"],
                                   fila["datos"][0]["day"]["condition"]["text"],
                                   fila["datos"][0]["day"]["condition"]["icon"]], axis=1)

df["day1"]=df.apply(lambda fila : [fila["datos"][1]["day"]["maxtemp_c"],
                                   fila["datos"][1]["day"]["mintemp_c"],
                                   fila["datos"][1]["day"]["daily_chance_of_rain"],
                                   fila["datos"][1]["day"]["condition"]["text"],
                                   fila["datos"][1]["day"]["condition"]["icon"]], axis=1)

df["day2"]=df.apply(lambda fila : [fila["datos"][2]["day"]["maxtemp_c"],
                                   fila["datos"][2]["day"]["mintemp_c"],
                                   fila["datos"][2]["day"]["daily_chance_of_rain"],
                                   fila["datos"][2]["day"]["condition"]["text"],
                                   fila["datos"][2]["day"]["condition"]["icon"]], axis=1)

df.drop(["coord","datos"], axis=1, inplace=True)


## y guardamos el dataset limpito en un csv:

df.to_csv("DATA/clean_info.csv")

## listo!