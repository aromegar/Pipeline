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
    