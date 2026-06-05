from django.urls import path
from . import views

urlpatterns = [
    path('mercados/', views.listar_mercados),
    path('mercados/<int:id>/', views.detalhes_mercado),
    path('usuarios/<int:id>/', views.detalhes_usuario),
    path('usuarios/criar/', views.criar_usuario),
    path('mercados/criar/', views.criar_mercado),
    path('categorias/criar/', views.criar_categoria),
    path('comentarios/criar/', views.criar_comentario),
]