# functions.py

import pandas as pd  # Asegúrate de importar las bibliotecas necesarias

# Cargar los datos CSV
df_reviews = pd.read_csv("data/output/reviews.csv")
df_items = pd.read_parquet("data/output/items.parquet")
df_steam_games = pd.read_csv("data/output/steam_games.csv")
def userdata(user_id: str):
    # Convierte user_id a tipo str
    user_id = str(user_id)
    
    # Filtra las compras del usuario en df_items
    compras_usuario = df_items[df_items['user_id'] == user_id]
    
    # Combina la información de las compras con los datos de los juegos en df_steam_games
    compras_usuario = pd.merge(compras_usuario, df_steam_games, left_on='item_id', right_on='id', how='inner')

    # Asegura que 'price' sea tratada como tipo numérico (para evitar errores de suma)
    compras_usuario['price'] = pd.to_numeric(compras_usuario['price'], errors='coerce')
    
    # Calcula el gasto total del usuario
    gasto_total = compras_usuario['price'].sum()
    
    # Filtra las revisiones del usuario en df_reviews
    revisiones_usuario = df_reviews[(df_reviews['user_id'] == user_id) & (df_reviews['item_id'].isin(compras_usuario['item_id']))]
    
    # Calcula el porcentaje de recomendación positiva
    porcentaje_recomendacion = (revisiones_usuario['recommend'].sum() / len(revisiones_usuario)) * 100
    
    # Calcula la cantidad de ítems comprados
    cantidad_items = len(compras_usuario)
    
    # Devuelve las estadísticas
    return {
        'Gasto Total': round(gasto_total, 2),
        'Porcentaje de Recomendación Promedio': porcentaje_recomendacion,
        'Cantidad de Ítems': cantidad_items
    }

def UserForGenre(genero: str):
    # Filtrar df_steam_games para obtener solo las filas que contienen el género especificado
    filtered_games = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]
    
    # Filtrar df_items para reducir el conjunto de datos a las columnas necesarias
    df_items_filtered = df_items[['user_id', 'item_id', 'playtime_forever']]
    
    # Combinar los DataFrames filtrados en uno solo usando "item_id" como clave
    combined_df = pd.merge(df_items_filtered, filtered_games, left_on='item_id', right_on='id', how='inner')

    # Asegura que 'playtime_forever' sea tratada como tipo numérico (para evitar errores de suma)
    combined_df['playtime_forever'] = pd.to_numeric(combined_df['playtime_forever'], errors='coerce')

    # Agrupa por usuario y año, suma las horas jugadas y encuentra el usuario con más horas jugadas
    result_df = combined_df.groupby(['user_id', 'release_date'])['playtime_forever'].sum().reset_index()
    max_user = result_df.loc[result_df['playtime_forever'].idxmax()]

    # Asegura que 'playtime_forever' sea tratada como tipo numérico (para evitar errores en el cálculo de acumulación)
    result_df['playtime_forever'] = pd.to_numeric(result_df['playtime_forever'], errors='coerce')

    # Convierte las horas jugadas de minutos a horas
    result_df['playtime_forever'] = result_df['playtime_forever'] / 60
    result_df['playtime_forever'] = result_df['playtime_forever'].round(0)

    # Crea una lista de acumulación de horas jugadas por año
    accumulation = result_df.groupby('release_date')['playtime_forever'].sum().reset_index()
    accumulation = accumulation.rename(columns={'release_date': 'Año', 'playtime_forever': 'Horas'})
    accumulation_list = accumulation.to_dict(orient='records')

    return {"Usuario con más horas jugadas para el género " + genero: max_user['user_id'], "Horas jugadas": accumulation_list}
