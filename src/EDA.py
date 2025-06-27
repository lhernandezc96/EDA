import pandas as pd
import numpy as np
import json
import re

# Leer JSON generado previamente
with open("EDA/src/data/personajes_completos.json", encoding="utf-8") as f:
    data = json.load(f)

# Leer archivo de IDs de personajes
char_ids = pd.read_csv("EDA/src/data/characters.csv")
name_to_id = dict(zip(char_ids["Character Name"], char_ids["Character ID"]))

# Crear estructuras
char_movie_time = {}
movie_lengths = {}

for entry in data:
    titulo = entry["titulo"]
    tipo = entry["tipo"]
    personajes = entry["personajes"]

    # Definir duración ficticia para el campo "Serie"
    movie_lengths[titulo] = 300 if tipo == "serie" else 120

    tiempos = {}
    for pj in personajes:
        nombre = pj["personaje"]
        tiempo = pj["tiempo"]
        tiempos[nombre] = tiempo
    char_movie_time[titulo] = tiempos

# Crear DataFrame
df = pd.DataFrame(char_movie_time)

# Función para convertir a minutos
def to_minutes(value):
    if pd.isna(value):
        return 0
    value = str(value).strip()
    if re.match(r"^\d+:\d{1,2}$", value):
        m, s = map(int, value.split(':'))
        return m + s / 60
    elif re.match(r"^:\d{1,2}$", value):
        return int(value[1:]) / 60
    elif value.isdigit():
        return int(value)
    return 0

# Convertir valores a minutos antes de renombrar
df = df.applymap(to_minutes).fillna(0)

# Renombrar índices con Character ID
df.rename(index=name_to_id, inplace=True)

# Agrupar duplicados por Character ID (sumar tiempos de personajes repetidos)
df = df.groupby(df.index).sum()

# Añadir fila 'Serie'
df.loc['Serie'] = [movie_lengths.get(p, 0) > 200 for p in df.columns]

# Añadir fila 'Fase'
df.loc['Fase'] = 0
for col in df.columns:
    if col in df.loc[:, 'Iron Man':'Marvel Los Vengadores'].columns:
        df.loc['Fase', col] = 1
    elif col in df.loc[:, 'Marvel Los Vengadores':'Ant-Man'].columns:
        df.loc['Fase', col] = 2
    elif col in df.loc[:, 'Capitán América: Civil War':'Spider-Man: Lejos de casa'].columns:
        df.loc['Fase', col] = 3
    elif col in df.loc[:, 'Bruja Escarlata y Visión':'Guardianes de la Galaxia: Especial felices fiestas'].columns:
        df.loc['Fase', col] = 4

# Exportar variables
char_movie_matrix = df
movie_lengths = {k: int(v) for k, v in movie_lengths.items() if k in df.columns}
