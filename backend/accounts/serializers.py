from rest_framework import serializers

from .models import *
from .models import DEFAULT_STRING_LEN
from .models import DEFAULT_DECIMAL_DIGITS


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class MercadoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    titulo = serializers.CharField(max_length=DEFAULT_STRING_LEN)
    descricao = serializers.CharField(max_length=DEFAULT_STRING_LEN)
    data_encerramento = serializers.DateTimeField()
    liquidez_inicial = serializers.DecimalField(max_digits=DEFAULT_DECIMAL_DIGITS, decimal_places=2)
    ativo = serializers.BooleanField()
    criado_em = serializers.DateTimeField(read_only=True)
    
    criado_por = serializers.StringRelatedField(read_only=True)
    categorias = CategoriaSerializer(many=True, read_only=True)
