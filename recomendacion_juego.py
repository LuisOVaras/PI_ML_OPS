import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

# Cargar los datos
df_steam = pd.read_csv('data/output/steam_games.csv')

# Crear una copia del DataFrame para evitar modificar el original
df_steam_copy = df_steam.copy()

# Desanidar las columnas de género
df_steam_copy['genres'] = df_steam_copy['genres'].apply(eval)  # Convierte las listas de géneros en listas de Python
unique_genres = list(set(genre for sublist in df_steam_copy['genres'] for genre in sublist))

# Crear columnas binarias para cada género
mlb = MultiLabelBinarizer()
genre_features = pd.DataFrame(mlb.fit_transform(df_steam_copy['genres']), columns=mlb.classes_)

# Seleccionar solo las columnas binarias de género
genre_features_only = genre_features.copy()

# Función de recomendación
def recomendacion_juego(id_producto, num_recomendaciones=5):
    # Crea una copia de las características del juego seleccionado y la convierte en un arreglo de Numpy
    juego_seleccionado = np.array(genre_features_only.iloc[id_producto].values).reshape(1, -1)

    # Calcula la similitud coseno entre el juego seleccionado y todos los juegos en un solo paso
    similaridades = cosine_similarity(juego_seleccionado, genre_features_only)

    # Obtén los índices de los juegos más similares (excluyendo el juego seleccionado)
    juegos_similares_indices = similaridades.argsort()[0][-num_recomendaciones:][::-1]

    # Obtén los nombres de los juegos recomendados (excluyendo el juego seleccionado)
    juegos_recomendados = df_steam_copy.iloc[juegos_similares_indices, :]

    lista = [{"id": row['id'], "title": row['title']} for index, row in juegos_recomendados.iterrows()]

    return lista

