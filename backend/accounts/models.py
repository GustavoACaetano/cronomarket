from django.db import models
from django.conf import settings
from uuid import uuid4


# Create your models here.

DEFAULT_DECIMAL_DIGITS = 12
DEFAULT_STRING_LEN = 255

class Mercado(models.Model):
    titulo = models.CharField(max_length=DEFAULT_STRING_LEN)
    descricao = models.TextField(max_length=500)
    data_encerramento = models.DateField()
    regra_encerramento = models.CharField(max_length=DEFAULT_STRING_LEN)
    opcao_sucesso = models.CharField(max_length=DEFAULT_STRING_LEN)
    opcao_fracasso = models.CharField(max_length=DEFAULT_STRING_LEN)
    link_imagem = models.URLField(max_length=DEFAULT_STRING_LEN)
    ativo = models.BooleanField(default=True)
    liquidez_inicial = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)
    valor_total_sucesso = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)
    valor_total_fracasso = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)

    categorias = models.ManyToManyField(to='Categoria', related_name='mercados')

    def __str__(self) -> str:
        return self.titulo


class HistoricoMercado(models.Model):
    data_hora = models.DateTimeField()
    percentual_sucesso = models.FloatField()
    percentual_fracasso = models.FloatField()

    mercado = models.ForeignKey('Mercado', on_delete=models.CASCADE, related_name='historico')


class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)
    eh_admin = models.BooleanField(default=False)

    mercados = models.ManyToManyField(to='Mercado', through='Operacao', related_name='participantes')


class Comentario(models.Model):
    mensagem = models.TextField(max_length=500)
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)

    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)
    mercado = models.ForeignKey('Mercado', on_delete=models.CASCADE)


class Categoria(models.Model):
    nome = models.CharField(max_length=DEFAULT_STRING_LEN, unique=True)

    def __str__(self) -> str:
        return self.nome


class Operacao(models.Model):
    class TipoOperacao(models.IntegerChoices):
        COMPRA = (1, 'Compra')
        VENDA = (2, 'Venda')

    tipo = models.PositiveIntegerField(choices=TipoOperacao.choices)
    quantidade = models.PositiveIntegerField()
    data_hora = models.DateTimeField(auto_now_add=True, editable=False)
    preco_medio = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)
    valor_total = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)

    mercado = models.ForeignKey('Mercado', on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)


class Resultado(models.Model):
    sucesso = models.BooleanField()

    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)
    mercado = models.OneToOneField('Mercado', on_delete=models.CASCADE, related_name='resultado')


class Acao(models.Model):
    quantidade = models.PositiveIntegerField()
    eh_sucesso = models.BooleanField()
    preco_medio = models.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)

    mercado = models.ForeignKey('Mercado', on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'mercado', 'eh_sucesso'],
                name='unique_acao_por_usuario_mercado_tipo'
            )
        ]

__all__ = ('Mercado', 'HistoricoMercado', 'Categoria', 'Usuario', 'Acao', 'Resultado',
            'Operacao', 'Comentario')
