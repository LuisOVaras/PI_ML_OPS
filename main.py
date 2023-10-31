from fastapi import FastAPI
import pandas as pd

app = FastAPI()


# Importar la función desde recomendacion_juego.py
from recomendacion_juego import recomendacion_juego

# Importar las funciones desde functions.py
from functions import userdata, UserForGenre, analyze_developer_data, analyze_developer_reviews, best_developer_year


# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")

# Ruta para obtener recomendaciones de juegos
@app.get("/recomendacion_juego/{id_producto}")
async def get_recomendacion_juego(id_producto: int):
    """Ingresa el ID de un Juego y te recomendara 5 similares."""

    result = recomendacion_juego(id_producto)  # Llama a la función de recomendación

    return {"recomendaciones": result}

@app.get('/developer_data/{desarrolladora}')
def developer(desarrolladora: str):
    resultado = analyze_developer_data( desarrolladora)
    return resultado


@app.get("/user_data/{user_id}")
async def get_user_data(user_id: str):
    result = userdata(user_id)
    return result


@app.get("/user_genre/{genero}")
async def get_user_genre(genero: str):
    result = UserForGenre(genero)
    return result


@app.get('/developer_reviews/{desarrolladora}')
def developer(desarrolladora: str):
    resultado = analyze_developer_reviews( desarrolladora)
    return resultado

@app.get("/best_developer/{año}")
def get_best_developers(year: int):
    resultado = best_developer_year(year)
    return {"Top 3 desarrolladores para el año {}: ".format(year): resultado}

#Run server
# uvicorn main:app --reload