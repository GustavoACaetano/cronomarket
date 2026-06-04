from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *
from .models import DEFAULT_STRING_LEN
from .models import DEFAULT_DECIMAL_DIGITS

# Deixei o saldo default sendo 100. Não sei se é aqui o lugar pra isso
DEFAULT_SALDO = 100.00

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

# tive que fazer isso para serializar o user dentro da classe usuario. obrigado brunetti.
class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user
    
class UsuarioSerializer(serializers.ModelSerializer):
    dados_usuario = DjangoUserSerializer(source='user')
    class Meta:
        model = Usuario
        fields = ['id', 'dados_usuario']

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = DjangoUserSerializer().create(user)
        usuario = Usuario.objects.create(user=user, saldo=DEFAULT_SALDO)
        return usuario