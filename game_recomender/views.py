from django.shortcuts import render, redirect
import os
import aiohttp
import asyncio
from django.conf import settings
from asgiref.sync import sync_to_async
from django.shortcuts import redirect
from urllib.parse import urlencode
from openid.consumer.consumer import Consumer, SUCCESS
from openid.store.memstore import MemoryStore
import re
from .utils import (
     recomendar_juegos_por_genero_y_tags,
    AsyncSteamService
)
import datetime

def steam_login(request):
    # Construye la URL OpenID de Steam
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': request.build_absolute_uri('/steam/callback/'),
        'openid.realm': request.build_absolute_uri('/'),
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }

    steam_url = 'https://steamcommunity.com/openid/login?' + urlencode(params)
    return redirect(steam_url)



def steam_callback(request):
    store = MemoryStore()
    consumer = Consumer(request.session, store)

    openid_response = consumer.complete(dict(request.GET.items()), request.build_absolute_uri())

    if openid_response.status == SUCCESS:
        claimed_id = openid_response.getDisplayIdentifier()
        match = re.search(r'https://steamcommunity.com/openid/id/(\d+)', claimed_id)
        if match:
            steam_id = match.group(1)
            request.session['steam_id'] = steam_id
            return redirect('perfil_completo_async')
        else:
            return render(request, 'game_recomender/accounts/error.html', {'error': 'SteamID no válido'})
    else:
        return render(request, 'game_recomender/accounts/error.html', {'error': 'Error de autenticación con Steam'})
    

def login_page(request):
    return render(request, 'game_recomender/login.html')



async def perfil_completo_async(request):
    steam_id = await sync_to_async(lambda: request.session.get('steam_id'))()
    if not steam_id:
        return await sync_to_async(render)(request, 'game_recomender/accounts/error.html', {'error': 'No autenticado con Steam'})

    api_key = os.getenv('STEAM_API_KEY') or getattr(settings, 'STEAM_API_KEY', None)
    if not api_key:
        return await sync_to_async(render)(request, 'game_recomender/accounts/error.html', {'error': 'No se encontró la API Key de Steam'})

    async with aiohttp.ClientSession() as session:
        steam_service = AsyncSteamService(api_key, session)
        # Obtener perfil y juegos en paralelo usando la clase
        perfil, juegos = await asyncio.gather(
            steam_service.get_profile(steam_id),
            steam_service.get_games(steam_id)
        )
        if not perfil or not juegos:
            return await sync_to_async(render)(request, 'game_recomender/accounts/error.html', {'error': 'No se pudo obtener información de Steam'})

        # Ordenar y tomar el top 10
        juegos.sort(key=lambda x: x.get('playtime_forever', 0), reverse=True)
        juegos_top = juegos
        perfil['fecha_creacion'] = datetime.datetime.fromtimestamp(perfil['timecreated']).strftime('%Y-%m-%d')
        # Enriquecer los juegos con géneros y etiquetas (en paralelo)
        tasks = [steam_service.get_game_details(juego['appid']) for juego in juegos_top]
        detalles_list = await asyncio.gather(*tasks)
        for juego, detalles in zip(juegos_top, detalles_list):
            juego['genre'] = detalles.get('genre', '')
            juego['popular_tags'] = detalles.get('popular_tags', '')

        for juego in juegos_top:
            juego['playtime_hours'] = round(juego.get('playtime_forever', 0) / 60, 1)

        recomendaciones = recomendar_juegos_por_genero_y_tags(juegos_top, top_n=30)
       
       

    return await sync_to_async(render)(request, 'game_recomender/perfil_completo_test.html', {
        'perfil': perfil,
        'juegos': juegos_top,
        'recomendaciones': recomendaciones
    })

