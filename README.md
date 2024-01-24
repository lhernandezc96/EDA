# MCU Screen Time EDA

Este repositorio contiene un Análisis Exploratorio de Datos (EDA) sobre el tiempo en pantalla de los personajes del Universo Cinematográfico de Marvel (MCU).

## Objetivo

El objetivo principal de este análisis es explorar y visualizar la distribución del tiempo en pantalla de los personajes a lo largo de las películas y series del MCU. Se han utilizado datos recopilados de una lista de IMDb creada por ninewheels0.

## Obtención de Datos

Los datos se obtuvieron mediante web scraping de la página de IMDb, utilizando la biblioteca BeautifulSoup en Python. Se extrajo información como el tiempo en pantalla de cada personaje, nombres de películas y series, y duración de cada título.

## Preprocesamiento de Datos

Durante el preprocesamiento, se limpiaron los datos y se manejaron casos en los que un mismo personaje tenía diferentes nombres en distintas películas/series. Se creó un CSV con nombres asociados a un único identificador.

## Funcionalidades del Análisis

El análisis incluye varias funciones para generar gráficas interactivas:

1. **Top Personajes por Tiempo en Pantalla:** Gráfica de los x personajes con más horas en pantalla en total.
2. **Top Personajes por Apariciones:** Gráfica de los x personajes con más apariciones en títulos diferentes.
3. **Tiempo en Pantalla por Título:** Gráfica de los títulos diferentes y las horas en pantalla del personaje seleccionado.
4. **Distribución del Tiempo en Pantalla:** Gráfico de tarta que representa el tiempo en pantalla de cada personaje en un título seleccionado.

## Personalización y Filtros

Todas las funciones permiten personalizar las gráficas, eligiendo entre películas y series, así como seleccionar combinaciones específicas de las cuatro fases del MCU.

## Uso del Repositorio

El código está organizado en funciones y se utiliza Streamlit para presentar las visualizaciones de manera interactiva.

## Lineas Futuras

Se plantea la posibilidad de expandir el análisis a otras sagas cinematográficas y televisivas, así como realizar un análisis más exhaustivo, buscando correlaciones y patrones en los datos.

---

**Nota:** Este README proporciona una visión general del proyecto. Consulta el código fuente y la documentación interna para detalles específicos.

