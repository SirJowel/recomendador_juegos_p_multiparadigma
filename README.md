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
