from collections import OrderedDict
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from EDA import char_movie_matrix, movie_lengths


def matriz_datos(no_serie, fases):
    columnas_seleccionadas = char_movie_matrix.columns[char_movie_matrix.loc['Fase'].isin(fases)]
    data_f = char_movie_matrix[columnas_seleccionadas]
    if no_serie:
        columnas_a_excluir = data_f.columns[data_f.loc['Serie'] == False]
        data = data_f[columnas_a_excluir]
    else:
        data = data_f

    data = data[(data != 0).any(axis=1)]
    data['Suma'] = data.sum(axis=1)
    data = data.sort_values(by='Suma', ascending=False)
    data = data.drop(columns='Suma')

    return data


def generar_grafico_barras_df(cantidad, no_serie, fases):
    data = matriz_datos(no_serie, fases)
    data['Total de tiempo en pantalla'] = data.sum(axis=1, skipna=True)
    data = data.sort_values(by='Total de tiempo en pantalla', ascending=False)
    data = data[data['Total de tiempo en pantalla'] != 0].head(cantidad)

    df = pd.DataFrame({
        'Personaje': data.index,
        'Tiempo total en pantalla': data['Total de tiempo en pantalla']
    })

    fig = px.bar(
        df,
        x='Personaje',
        y='Tiempo total en pantalla',
        title='Tiempo total en pantalla de los personajes',
        labels={'Personaje': 'Personaje', 'Tiempo total en pantalla': 'Tiempo total en pantalla'},
        color_discrete_sequence=['rgb(179, 39, 14)'],
        hover_data={'Personaje': True, 'Tiempo total en pantalla': True},
    )

    fig.update_layout(title=dict(text='Tiempo total en pantalla de los personajes', font=dict(size=24)))
    fig.update_traces(hovertemplate='Personaje: %{x}<br>Tiempo total en pantalla: %{y}')
    fig.update_layout(height=500, width=900)

    return fig


def apariciones_pj(no_serie, fases):
    data = matriz_datos(no_serie, fases)
    apariciones_pj = OrderedDict()

    for pj in data.index:
        fila = data.loc[pj]
        columnas_no_cero = fila[(fila != 0) & (fila.map(lambda x: isinstance(x, (int, float))))].index.tolist()
        apariciones_pj[pj] = columnas_no_cero

    return apariciones_pj


def generar_grafico_barras_num_apariciones(cantidad, fases, no_serie=False):
    ordenado_por_longitud = OrderedDict(
        sorted(apariciones_pj(no_serie, fases).items(), key=lambda x: len(x[1]), reverse=True)
    )

    claves = list(ordenado_por_longitud.keys())[:cantidad]
    longitudes = [len(ordenado_por_longitud[clave]) for clave in claves]

    df = pd.DataFrame({'Personaje': claves, 'Apariciones': longitudes})

    fig = px.bar(
        df,
        x='Personaje',
        y='Apariciones',
        title='Nº total de apariciones de los personajes',
        labels={'Personaje': 'Personaje', 'Apariciones': 'Apariciones'},
        color_discrete_sequence=['rgb(179, 39, 14)'],
        hover_data={'Personaje': True, 'Apariciones': True},
    )

    fig.update_layout(title=dict(text='Nº total de apariciones de los personajes', font=dict(size=24)))
    fig.update_traces(hovertemplate='Personaje: %{x}<br>Nº de apariciones: %{y}')
    fig.update_layout(height=500, width=900)

    return fig


def generar_grafico_peliculas_del_char(char, fases, no_serie=False):
    columnas_seleccionadas = char_movie_matrix.columns[char_movie_matrix.loc['Fase'].isin(fases)]
    data_f = char_movie_matrix[columnas_seleccionadas]

    peliculas = {peli: data_f.loc[char, peli] for peli in apariciones_pj(no_serie, fases).get(char, [])}

    df = pd.DataFrame(list(peliculas.items()), columns=['Pelicula', 'Tiempo en pantalla'])
    suma_total = df['Tiempo en pantalla'].sum()

    fig = px.bar(
        df,
        x='Pelicula',
        y='Tiempo en pantalla',
        title=f'{char} ({suma_total:.2f} minutos en total)',
        color_discrete_sequence=['rgb(179, 39, 14)'],
        labels={'Pelicula': 'Peliculas', 'Tiempo en pantalla': 'Tiempo en pantalla'},
        hover_data={'Pelicula': True, 'Tiempo en pantalla': True},
    )

    fig.update_traces(hovertemplate='Pelicula: %{x}<br>Tiempo en pantalla: %{y} mins')
    fig.update_layout(height=400, width=800)

    return fig


def grafico_pie_t_pantalla(pelicula):
    df = char_movie_matrix[char_movie_matrix[pelicula] != 0]
    df[pelicula] = pd.to_numeric(df[pelicula], errors='coerce')

    pie1_list = df[pelicula].round(2).tolist()
    labels = df.index

    top5_indices = df[pelicula].nlargest(5).index
    custom_labels = [name if name in top5_indices else '' for name in labels]

    colores_rgba = list(reversed(px.colors.sequential.Reds))

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'pie'}]])
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=pie1_list,
            textinfo='text+value',
            hoverinfo="label+value",
            marker=dict(colors=colores_rgba),
            hole=0.3,
            text=custom_labels,
        ),
        row=1, col=1
    )

    fig.update_layout(
        title=dict(text=f"Tiempo en pantalla en {pelicula} ({movie_lengths[pelicula]})", font=dict(size=24)),
        annotations=[{
            "font": {"size": 20},
            "showarrow": False,
            "text": pelicula,
            "x": 0.5,
            "y": 1.07,
        }],
        height=700,
        width=900,
    )

    return fig