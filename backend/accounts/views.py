from django.shortcuts import get_object_or_404
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
@api_view(['POST'])
def criar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    usuario = serializer.save()
    return Response(UsuarioSerializer(usuario).data, status=201)
    
    
@api_view(['GET'])
def detalhes_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)