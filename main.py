from fastapi import FastAPI
import pandas as pd

app = FastAPI()


# Importar la función desde recomendacion_juego.py
from recomendacion_juego import recomendacion_juego

# Importar las funciones desde functions.py
from functions import userdata, UserForGenre

# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_parquet("data/output/items.parquet")
df_steam_games = pd.read_csv("data/output/steam_games.csv")

# Ruta para obtener recomendaciones de juegos
@app.get("/recomendacion_juego/{id_producto}")
async def get_recomendacion_juego(id_producto: int):
    """Ingresa el ID de un Juego y te recomendara 5 similares."""

    result = recomendacion_juego(id_producto)  # Llama a la función de recomendación

    return {"recomendaciones": result}

# 2
@app.get("/user_data/{user_id}")
async def get_user_data(user_id: str):
    result = userdata(user_id)
    return result

# 3
@app.get("/user_genre/{genero}")
async def get_user_genre(genero: str):
    result = UserForGenre(genero)
    return result

# 5 Aquí desarrollamos el ultimo endpoint:
@app.get("/developer/{desarrolladora}")
def developer(desarrolladora: str):
    # Filtrar las reseñas por el desarrollador dado
    reseñas_desarrolladora = df_reviews[df_reviews['user_id'].isin(df_items[df_items['item_id'].isin(df_steam_games[df_steam_games['developer'] == desarrolladora]['id'])]['user_id'])]

    # Contar las reseñas con sentimiento positivo y negativo
    sentimiento_positivo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 2].shape[0]
    sentimiento_negativo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 0].shape[0]

    # Crear el diccionario de resultados
    resultado = {desarrolladora: {'Positive': sentimiento_positivo, 'Negative': sentimiento_negativo}}

    return resultado

#Run server
# uvicorn main:app --reload