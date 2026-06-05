from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'comentarios', views.ComentarioViewSet)

urlpatterns = [
    path('mercados/', views.listar_mercados),
    path('mercados/<int:id>/', views.detalhes_mercado),
    path('usuarios/<int:id>/', views.detalhes_usuario),
    path('usuarios/criar/', views.criar_usuario),
    path('mercados/criar/', views.criar_mercado),
    path('categorias/criar/', views.criar_categoria),
    path('', include(router.urls)),
]
