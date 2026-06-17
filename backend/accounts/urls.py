from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'comentarios', views.ComentarioViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'mercados', views.MercadoViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'acoes', views.AcaoViewSet)
router.register(r'operacoes', views.OperacaoViewSet)
router.register(r'resultados', views.ResultadoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('csrf/', views.GetCSRFToken.as_view(), name='csrf'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]
