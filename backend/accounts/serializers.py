from django.conf import settings
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

# tive que fazer isso para serializar o user dentro da classe usuario. obrigado brunetti.
class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'email']

        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = settings.AUTH_USER_MODEL.objects.create_user(**validated_data)
        return user
    
class UsuarioSerializer(serializers.ModelSerializer):
    dados_usuario = DjangoUserSerializer(source='user')
    class Meta:
        model = Usuario
        fields = ['id', 'dados_usuario', 'saldo', 'eh_admin']

    def create(self, validated_data):
        user = validated_data.pop('dados_usuario')
        user = DjangoUserSerializer().create(user)
        usuario = Usuario.objects.create(user=user, saldo=validated_data['saldo'], eh_admin=validated_data['eh_admin'])
        return usuario