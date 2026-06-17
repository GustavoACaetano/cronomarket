from dataclasses import fields

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *
from .models import DEFAULT_STRING_LEN
from .models import DEFAULT_DECIMAL_DIGITS

DEFAULT_SALDO = 300.00


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']
    
    def create(self, validated_data):
        categoria = Categoria.objects.create(**validated_data)
        return categoria


class MercadoSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(many=True, queryset=Categoria.objects.all(), required=False)

    class Meta:
        model = Mercado
        fields = ['id', 'titulo', 'descricao', 'data_encerramento', 'ativo', 'liquidez_inicial', 'valor_total_sucesso', 'valor_total_fracasso', 'regra_encerramento', 'opcao_sucesso', 'opcao_fracasso', 'link_imagem', 'categorias']

        extra_kwargs = {
            'id' : {'read_only': True},
            'valor_total_sucesso': {'read_only': True},
            'valor_total_fracasso': {'read_only': True},
        }

    def create(self, validated_data):
        categorias_ids = validated_data.pop('categorias', [])
        mercado = Mercado.objects.create(**validated_data, valor_total_sucesso=0, valor_total_fracasso=0)

        if categorias_ids:
            mercado.categorias.set(categorias_ids)

        return mercado

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
        fields = ['id', 'dados_usuario', 'saldo', 'eh_admin']
        extra_kwargs = {
            'saldo': {'read_only': True},
            'eh_admin': {'read_only': True},
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = DjangoUserSerializer().create(user)
        usuario = Usuario.objects.create(user=user, saldo=DEFAULT_SALDO)
        return usuario


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        User = get_user_model()

        try:
            # Try to lookup user by email
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            try:
                # If email lookup fails, check if the input matches username directly
                user_obj = User.objects.get(username=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = email

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError('Usuário/Email ou senha inválidos.')

        attrs['user'] = user
        return attrs
    

class ComentarioSerializer(serializers.ModelSerializer):
    mercado = serializers.PrimaryKeyRelatedField(queryset=Mercado.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    username = serializers.CharField(source='usuario.user.username', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'mensagem', 'criado_em', 'usuario', 'username', 'mercado']


class AcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acao
        fields = ['id', 'quantidade', 'eh_sucesso', 'preco_medio', 'mercado', 'usuario']


class OperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacao
        fields = ['id', 'tipo', 'quantidade', 'data_hora', 'preco_medio', 'valor_total', 'mercado', 'usuario']


class HistoricoMercadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoMercado
        fields = ['id', 'data_hora', 'percentual_sucesso', 'percentual_fracasso', 'mercado']


class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = ['id', 'sucesso', 'usuario', 'mercado']

