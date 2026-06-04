from django.urls import path
from . import views

urlpatterns = [
    path('mercados/', views.listar_mercados),
    path('mercados/<int:id>/', views.detalhes_mercado),
    path('usuario/', views.criar_usuario, views.listar_usuario),
]