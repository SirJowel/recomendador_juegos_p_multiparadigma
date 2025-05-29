"""
README DEL PROYECTO: Recomendador de Juegos Steam (Multiparadigma)

Este proyecto es una aplicación web desarrollada en Django que permite a los usuarios autenticarse con Steam, visualizar su perfil y biblioteca de juegos, y obtener recomendaciones personalizadas basadas en géneros y etiquetas de sus juegos más jugados.

====================
FUNCIONES Y VISTAS PRINCIPALES
====================

# game_recomender/views.py

def steam_login(request):
    """
    Redirige al usuario a la página de autenticación de Steam usando OpenID.
    Construye la URL de login de Steam y redirige al usuario para iniciar sesión.
    """
    # ...existing code...

def steam_callback(request):
    """
    Recibe la respuesta de Steam tras el login OpenID.
    Si la autenticación es exitosa, guarda el steam_id en sesión y redirige al perfil.
    Si falla, muestra un error.
    """
    # ...existing code...

def login_page(request):
    """
    Renderiza la página de login con el botón de Steam.
    """
    # ...existing code...

async def perfil_completo_async(request):
    """
    Vista asíncrona que obtiene el perfil y la biblioteca de juegos del usuario desde Steam.
    - Obtiene el steam_id de la sesión.
    - Usa AsyncSteamService para obtener perfil y juegos en paralelo.
    - Enriquecer cada juego con género y etiquetas populares.
    - Calcula las horas jugadas y la fecha de creación del perfil.
    - Llama a la función de recomendación personalizada.
    - Renderiza el template 'perfil_completo_test.html' con los datos.
    """
    # ...existing code...

====================
UTILIDADES PRINCIPALES
====================

# game_recomender/utils.py

class AsyncSteamService:
    """
    Servicio asíncrono para interactuar con la API de Steam.
    Métodos:
    - get_profile(steam_id): Devuelve el perfil del usuario.
    - get_games(steam_id): Devuelve la lista de juegos del usuario.
    - get_game_details(appid): Devuelve detalles de un juego (género, etiquetas, etc).
    """
    # ...existing code...

def recomendar_juegos_por_genero_y_tags(juegos, top_n=30):
    """
    Recibe una lista de juegos y recomienda los top_n juegos más relevantes
    según géneros y etiquetas populares en la biblioteca del usuario.
    """
    # ...existing code...

====================
TEMPLATES PRINCIPALES
====================

# game_recomender/templates/game_recomender/login.html
- Muestra el botón para iniciar sesión con Steam.
- Extiende de 'game_recomender/base.html'.

# game_recomender/templates/game_recomender/perfil_completo_test.html
- Muestra el perfil del usuario (avatar, nombre, país, estado, fecha de creación).
- Lista la biblioteca de juegos con imagen, nombre, horas jugadas, género y etiquetas.
- Muestra recomendaciones personalizadas.

# game_recomender/templates/game_recomender/accounts/error.html
- Muestra mensajes de error amigables si ocurre algún problema en la autenticación o la obtención de datos.

# game_recomender/templates/game_recomender/base.html
- Plantilla base con estilos y estructura general para todas las páginas.

====================
ARCHIVOS Y ESTRUCTURA
====================

- core/settings.py: Configuración principal de Django, rutas de templates, apps instaladas, etc.
- core/urls.py: Rutas principales del proyecto, incluye las URLs de la app game_recomender.
- game_recomender/urls.py: Rutas de la app (login, callback, perfil, etc).
- requirements.txt: Dependencias del proyecto.
- .gitignore: Excluye venv, .env y archivos temporales del repositorio.
- README.md: Documentación general y pasos de instalación.

====================
NOTAS DE USO
====================
- El usuario debe tener su perfil de Steam y detalles de juego en modo público para que la app funcione correctamente.
- El archivo .env debe contener la clave STEAM_API_KEY.
- El entorno virtual y el archivo .env están excluidos del repositorio por seguridad.

====================

Desarrollado para la materia de Programación Multiparadigma.
# Recomendador de Juegos Steam (Multiparadigma)

Este proyecto es un recomendador de juegos basado en la biblioteca de Steam de un usuario, desarrollado en Django.

## Características
- Login con Steam (OpenID)
- Visualización de perfil y biblioteca de juegos
- Recomendaciones personalizadas por géneros y etiquetas

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/<tu_usuario>/recomendador_juegos_p_multiparadigma.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` con tu clave de API de Steam:
   ```env
   STEAM_API_KEY=tu_clave_aqui
   ```
4. Ejecuta las migraciones y el servidor:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Estructura
- `core/` - Configuración principal de Django
- `game_recomender/` - Lógica de la app y vistas
- `templates/` - Plantillas HTML

## Notas
- El directorio `venv/` y el archivo `.env` están excluidos del repositorio por seguridad.

---

Desarrollado para la materia de Programación Multiparadigma.
