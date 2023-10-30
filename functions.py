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


# Se desarrolla la función UserForGenre
def UserForGenre(genero: str):
    # Filtra df_steam_games para obtener solo las filas que contienen el género especificado
    filtered_games = df_steam_games[df_steam_games['genres'].str.contains(genero, case=False, na=False)]

    # Filtra df_items para reducir el conjunto de datos a las columnas necesarias
    df_items_filtered = df_items[df_items['item_id'].isin(filtered_games['id'])]

    # Realiza una unión (join) para incluir la información de 'release_date' desde df_steam_games
    df_items_filtered = df_items_filtered.merge(filtered_games[['id', 'release_date']], left_on='item_id', right_on='id', how='inner')

    # Verifica si 'release_date' está en el DataFrame df_items_filtered
    if 'release_date' not in df_items_filtered.columns:
        return {"Error": "La columna 'release_date' no está presente en el DataFrame."}

    # Continúa con la operación de agrupación
    result_df = df_items_filtered.groupby(['user_id', 'release_date'])['playtime_forever'].sum().reset_index()
    max_user = result_df.loc[result_df['playtime_forever'].idxmax()]

    # Convierte las horas jugadas de minutos a horas
    result_df['playtime_forever'] = (result_df['playtime_forever'] / 60).round(0)

    # Crea una lista de acumulación de horas jugadas por año
    accumulation = result_df.groupby('release_date')['playtime_forever'].sum().reset_index()
    accumulation = accumulation.rename(columns={'release_date': 'Año', 'playtime_forever': 'Horas'})
    accumulation_list = accumulation.to_dict(orient='records')

    return {"Usuario con más horas jugadas para el género " + genero: max_user['user_id'], "Horas jugadas": accumulation_list}

def analyze_developer_data(desarrolladora: str):
    # Creamos un DataFrame más reducido
    df_end1 = df_steam_games.loc[:,['developer', 'id', 'price','release_date']]
    # Utiliza el método str.split para dividir la fecha en sus componentes (Año, Mes, Día) dejando solo el año
    df_end1['release_date'] = df_end1['release_date'].str.split('-').str.get(0)
    # Filtra el DataFrame para los juegos de la empresa desarrolladora especificada
    juegos_desarrolladora = df_end1[df_end1['developer'] == desarrolladora]
    # Agrupa por año y cuenta la cantidad de juegos
    juegos_por_ano = juegos_desarrolladora.groupby('release_date').size().reset_index(name='Cantidad de Items')
    # Filtra los juegos gratuitos
    juegos_gratuitos = juegos_desarrolladora[juegos_desarrolladora['price'] == 0]
    # Agrupa los juegos gratuitos por año y cuenta la cantidad
    juegos_gratuitos_por_ano = juegos_gratuitos.groupby('release_date').size().reset_index(name='cantidad_juegos_gratuitos')
    # Combina los datos de juegos totales y juegos gratuitos por año
    resultado = pd.merge(juegos_por_ano, juegos_gratuitos_por_ano, on='release_date', how='left')
    # Rellena los valores nulos en juegos gratuitos con 0
    resultado['cantidad_juegos_gratuitos'].fillna(0, inplace=True)
    # Calcula el porcentaje de juegos gratuitos por año
    resultado['porcentaje_juegos_gratuitos'] = (resultado['cantidad_juegos_gratuitos'] / resultado['Cantidad de Items']) * 100
    # Elimina la columna 'cantidad_juegos_gratuitos'
    resultado.drop(columns='cantidad_juegos_gratuitos', inplace=True)
    # Renombra las columnas
    resultado.rename(columns={'release_date': 'Año', 'porcentaje_juegos_gratuitos': 'Contenido Free'}, inplace=True)
    # Convierte la columna 'Cantidad de Items' a enteros y 'Contenido Free' a flotantes
    resultado['Cantidad de Items'] = resultado['Cantidad de Items'].astype(int)
    resultado['Contenido Free'] = resultado['Contenido Free'].astype(float)
    # Convierte el DataFrame a una lista de diccionarios para asegurarse de que los tipos de datos sean estándar de Python (evita errores en FastAPI)
    resultado_dict_list = resultado.to_dict(orient='records')
    return resultado_dict_list

def analyze_developer_reviews(desarrolladora: str):
    # Filtrar las reseñas por el desarrollador dado
    reseñas_desarrolladora = df_reviews[df_reviews['user_id'].isin(df_items[df_items['item_id'].isin(df_steam_games[df_steam_games['developer'] == desarrolladora]['id'])]['user_id'])]

    # Contar las reseñas con sentimiento positivo y negativo
    sentimiento_positivo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 2].shape[0]
    sentimiento_negativo = reseñas_desarrolladora[reseñas_desarrolladora['sentiment_analysis'] == 0].shape[0]

    # Crear el diccionario de resultados
    resultado = {desarrolladora: {'Positive': sentimiento_positivo, 'Negative': sentimiento_negativo}}

    return resultado