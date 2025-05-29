# accounts/utils.py
import pandas as pd
from functools import reduce


class AsyncSteamService:
    def __init__(self, api_key , session):
        self.api_key = api_key
        self.session = session  # Debe ser una instancia de aiohttp.ClientSession

    async def get_profile(self, steam_id):
        url = (
            f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'
            f'?key={self.api_key}&steamids={steam_id}'
        )
        async with self.session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if 'players' in data.get('response', {}) and len(data['response']['players']) > 0:
                return data['response']['players'][0]
            else:
                return None

    async def get_games(self, steam_id):
        url = (
            f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
            f'?key={self.api_key}&steamid={steam_id}'
            f'&include_appinfo=1&include_played_free_games=1'
        )
        async with self.session.get(url) as response:
            if response.status != 200:
                return []
            data = await response.json()
            if 'response' in data and 'games' in data['response']:
                return data['response']['games']
            else:
                return []

    async def get_achievements(self, steam_id, appid):
        url = (
            f'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/'
            f'?key={self.api_key}&steamid={steam_id}&appid={appid}'
        )
        async with self.session.get(url) as response:
            if response.status == 403:
                return {'error': 'El perfil o los logros de este juego no son públicos.'}
            if response.status != 200:
                return {'error': 'No se pudieron obtener los logros por un error de Steam.'}
            data = await response.json()
            if 'playerstats' in data and 'achievements' in data['playerstats']:
                return data['playerstats']['achievements']
            elif 'playerstats' in data and 'error' in data['playerstats']:
                return {'error': data['playerstats']['error']}
            else:
                return {'error': 'No se encontraron logros para este juego.'}

    async def get_game_details(self, appid):
        url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
        try:
            async with self.session.get(url, timeout=5) as response:
                if response.status != 200:
                    return {'genre': '', 'popular_tags': ''}
                data = await response.json()
                app_data = data.get(str(appid), {}).get('data', {})
                genres_list = app_data.get('genres', [])
                if isinstance(genres_list, list):
                    genres = ','.join([g.get('description', '') for g in genres_list if 'description' in g])
                else:
                    genres = ''
                categories_list = app_data.get('categories', [])
                if isinstance(categories_list, list):
                    tags = ','.join([c.get('description', '') for c in categories_list if 'description' in c])
                else:
                    tags = ''
                if 'steamspy_tags' in app_data:
                    tags = app_data['steamspy_tags']
                return {
                    'genre': genres,
                    'popular_tags': tags if isinstance(tags, str) else ','.join(tags) if isinstance(tags, list) else ''
                }
        except Exception as e:
            print(f'Error consultando {appid}: {e}')
            return {'genre': '', 'popular_tags': ''}



def recomendar_juegos_por_genero_y_tags(juegos_usuario, top_n=10):
    """
    Recomienda juegos basados en los géneros y etiquetas de los juegos jugados por el usuario.
    Utiliza programación funcional y pandas.
    """
    # Cargar el dataset de juegos
    df = pd.read_csv('steam_games.csv', low_memory=False)

    # Extraer appid de la url (soporta /app/, /bundle/ y /sub/)
    df['appid'] = df['url'].str.extract(r'/(?:app|bundle|sub)/(\d+)(?:/[^/]*)?/?$')

    # Filtrar solo juegos individuales (type = app)
    df = df[df['types'] == 'app']

    # Filtrar solo juegos con reseñas que empiecen con 'Very Positive'
    df = df[df['all_reviews'].str.startswith('Very Positive', na=False)]
    #df = df[df['recent_reviews'].str.startswith('Mostly Positive', na=False)]

    # Excluir juegos cuya descripción contenga 'DLC' (no sensible a mayúsculas)
    df = df[~df['game_description'].str.contains('DLC', case=False, na=False)]
    df = df[~df['popular_tags'].str.contains('Sexual', case=False, na=False)]
    df = df[~df['popular_tags'].str.contains('Nudity', case=False, na=False)]
    df = df[~df['popular_tags'].str.contains('Romance', case=False, na=False)]
    df = df[~df['popular_tags'].str.contains('Female', case=False, na=False)]

    # Obtener nombres y appids de juegos jugados
    nombres_jugados = set(map(lambda j: j.get('name', '').strip().lower(), juegos_usuario))

    # Extraer géneros y tags de los juegos jugados
    generos = list(filter(None, map(lambda j: j.get('genre', ''), juegos_usuario)))
    tags = list(filter(None, map(lambda j: j.get('popular_tags', ''), juegos_usuario)))

    # Unir todos los géneros y tags en sets
    set_generos = reduce(lambda a, b: a.union(set(map(str.strip, b.split(',')))), generos, set())
    set_tags = reduce(lambda a, b: a.union(set(map(str.strip, b.split(',')))), tags, set())

    # Función para filtrar juegos similares
    def es_similar(row):
        juego_generos = set(map(str.strip, str(row['genre']).split(',')))
        juego_tags = set(map(str.strip, str(row['popular_tags']).split(',')))
        return (
            len(set_generos & juego_generos) > 0 or
            len(set_tags & juego_tags) > 0
        )

    # Filtrar juegos que no ha jugado el usuario y que sean similares
    juegos_filtrados = (
        df[~df['name'].str.strip().str.lower().isin(nombres_jugados)]
          .pipe(lambda d: d[d.apply(es_similar, axis=1)])
    )

    if juegos_filtrados.empty:
        return []

    juegos_recomendados = juegos_filtrados.sample(n=min(top_n, len(juegos_filtrados)), random_state=42)

    # Seleccionar columnas relevantes
    columnas = ['appid', 'name', 'genre', 'popular_tags', 'desc_snippet', 'url']
    return juegos_recomendados[columnas].to_dict(orient='records')

