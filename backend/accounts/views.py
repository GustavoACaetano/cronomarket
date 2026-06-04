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
