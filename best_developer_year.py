import pandas as pd

df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_csv("data/output/items.csv")
df_steam_games = pd.read_csv("data/output/steam_games.csv")

def best_developer_year(año: int):
    # Filtra los juegos del año especificado en df_steam_games

    # Convierte la columna 'release_date' a datetime si aún no lo está
    df_steam_games['release_date'] = pd.to_datetime(df_steam_games['release_date'], errors='coerce')

    # Filtra los juegos por año
    juegos_del_año = df_steam_games[pd.to_datetime(df_steam_games['release_date']).dt.year == año]

    # Combinación de DataFrames para obtener los juegos recomendados en ese año
    combined_df = pd.merge(juegos_del_año, df_reviews, left_on='id', right_on='item_id', how='inner')

    # Filtra los juegos recomendados con comentarios positivos
    juegos_recomendados = combined_df[(combined_df['recommend'] == True) & (combined_df['sentiment_analysis'] == 2)]

    # Agrupa por desarrollador y cuenta las recomendaciones
    desarrolladores_recomendados = juegos_recomendados['developer'].value_counts().reset_index()
    desarrolladores_recomendados.columns = ['developer', 'recommend_count']

    # Ordena en orden descendente y toma los 3 principales
    top_desarrolladores = desarrolladores_recomendados.nlargest(3, 'recommend_count')

    # Formatea el resultado en un formato de lista de diccionarios
    resultado = [{"Puesto {}: {}".format(i + 1, row['developer']): row['recommend_count']} for i, row in top_desarrolladores.iterrows()]

    return resultado