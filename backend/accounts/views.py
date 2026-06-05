from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view()
def listar_mercados(request):
    queryset = Mercado.objects.filter(ativo=True)
    serializer = MercadoSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def detalhes_mercado(request, id):
    mercado = get_object_or_404(Mercado, pk=id)
    serializer = MercadoSerializer(mercado)
    return Response(serializer.data)

# eu gostaria de fazer uma API Restful aqui. Mas os nomes funcionam de um jeito burro. Too bad!
@extend_schema(request=UsuarioSerializer, responses={201: UsuarioSerializer})
@api_view(['POST'])
def criar_usuario(request: UsuarioSerializer):
    serializer = UsuarioSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    if Usuario.objects.filter(user__username=serializer.validated_data['user']['username']).exists():
        return Response({'error': 'Username já existe'}, status=400)
    
    if Usuario.objects.filter(user__email=serializer.validated_data['user']['email']).exists():
        return Response({'error': 'Email já existe'}, status=400)
    
    usuario = serializer.save()
    return Response(UsuarioSerializer(usuario).data, status=201)
    
@api_view(['GET'])
def detalhes_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@extend_schema(request=MercadoSerializer, responses={201: MercadoSerializer})
@api_view(['POST'])
def criar_mercado(request):
    serializer = MercadoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    mercado = serializer.save()
    return Response(MercadoSerializer(mercado).data, status=201)

@extend_schema(request=CategoriaSerializer, responses={201: CategoriaSerializer})
@api_view(['POST'])
def criar_categoria(request: CategoriaSerializer):
    serializer = CategoriaSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    categoria = serializer.save()
    return Response(CategoriaSerializer(categoria).data, status=201)

@extend_schema(request=ComentarioSerializer, responses={201: ComentarioSerializer})
@api_view(['POST'])
def criar_comentario(request: ComentarioSerializer):
    serializer = ComentarioSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    comentario = serializer.save()
    return Response(ComentarioSerializer(comentario).data, status=201)
