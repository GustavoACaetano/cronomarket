from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'comentarios', views.ComentarioViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'mercados', views.MercadoViewSet)
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
]
