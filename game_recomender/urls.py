from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.steam_login, name='steam_login'),
    path('callback/', views.steam_callback, name='steam_callback'),
    path('', views.login_page, name='login_page'),
    path('perfil_async/', views.perfil_completo_async, name='perfil_completo_async')
]
