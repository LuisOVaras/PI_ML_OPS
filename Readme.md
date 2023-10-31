# Proyecto de MLOps para Steam - Sistema de Recomendación de Videojuegos

Este proyecto de MLOps se centra en la creación de un sistema de recomendación de videojuegos para usuarios de la plataforma Steam. El objetivo es brindar a los usuarios recomendaciones personalizadas basadas en sus preferencias y patrones de juego. Para lograr esto, se ha seguido un proceso que abarca desde la recolección y limpieza de datos hasta la implementación de un sistema de recomendación y la exposición de la funcionalidad a través de una API.

## Contenido del Repositorio

- `data/`: En esta carpeta, encontrarás los conjuntos de datos utilizados en el proyecto. Estos datos han sido procesados previamente mediante ETL (Transformación, Carga y Limpieza) para asegurar que funcionen de manera efectiva tanto en FastAPI como en Render. Esto garantiza que los datos estén listos para su uso y análisis sin problemas.

- `functions.py`: Este archivo contiene las funciones que se utilizan en la API para proporcionar datos y recomendaciones a los usuarios.

- `recomendacion.py`: En este archivo se encuentra el código relacionado con el sistema de recomendación, que utiliza el algoritmo de similitud de coseno para recomendar juegos similares.

- `main.py`: Este es el archivo principal de la API FastAPI que expone los endpoints y proporciona acceso a la funcionalidad del sistema de recomendación.

- `requirements.txt`: El archivo que lista las bibliotecas de Python necesarias para ejecutar el proyecto.

## Tecnologías Utilizadas

El proyecto se ha desarrollado utilizando las siguientes tecnologías:

- [FastAPI](https://fastapi.tiangolo.com/): Un marco web moderno y rápido para Python que se utiliza para construir la API.

- [Pandas](https://pandas.pydata.org/): Una biblioteca de Python para el análisis y manipulación de datos.

- [scikit-learn](https://scikit-learn.org/stable/): Una biblioteca de aprendizaje automático de código abierto para Python que se utiliza en el sistema de recomendación.

## Endpoints de la API

El proyecto ofrece los siguientes endpoints a través de la API:

- `GET /userdata/{User_id}`: Devuelve información sobre un usuario, incluyendo el gasto total, el porcentaje de recomendación y la cantidad de juegos adquiridos.

- `GET /userforgenre/{genero}`: Proporciona información sobre el usuario que ha acumulado más horas jugadas para un género específico, junto con una lista de la acumulación de horas jugadas por año.

- `GET /best_developer_year/{anio}`: Devuelve una lista de los tres principales desarrolladores con juegos más recomendados por los usuarios para un año específico.

- `GET /developer_review/{desarrolladora}`: Proporciona un análisis de sentimiento de las reseñas de usuarios para una empresa desarrolladora, incluyendo la cantidad de reseñas positivas y negativas.

- `GET /developer/{desarrollador}`: Ofrece la cantidad de ítems y el porcentaje de contenido gratuito por año para una empresa desarrolladora específica.

- `GET /recomendacion_juego/{id_producto}`: Proporciona una lista de 5 juegos recomendados similares al juego con el ID especificado.

## Sistema de Recomendación

El sistema de recomendación se basa en el algoritmo de similitud de coseno y utiliza las preferencias de género de los juegos para recomendar juegos similares a los que el usuario ha jugado. El sistema tiene en cuenta la categoría de género de los juegos y recomienda aquellos que tienen una mayor similitud con los juegos previamente jugados por el usuario.

## Uso de la API

Para utilizar la API, puedes realizar consultas directamente en el sitio donde se hizo el deploy. La API está diseñada para proporcionar recomendaciones de juegos y datos sobre los usuarios y desarrolladores de Steam. Puedes acceder a la documentación y realizar consultas [aquí](https://pi-test.onrender.com/docs/).

## Video de Demostración

Para ver una demostración de la funcionalidad de la API y el sistema de recomendación en acción, puede ver el video de demostración [aquí](https://drive.google.com/drive/folders/1ZbpLziJw5X6BUVo9fa5_oQ1ETBWfJSIj?usp=sharing).
