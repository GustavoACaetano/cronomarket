from django.contrib import admin
from . import models


@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'saldo', 'eh_admin')
    search_fields = ('user__username', 'user__email')
    list_filter = ('eh_admin',)


@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(models.Mercado)
class MercadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_encerramento', 'liquidez_inicial', 'ativo')
    autocomplete_fields = ('categorias',)
    search_fields = ('titulo', 'descricao')
    list_filter = ('categorias', 'ativo')
