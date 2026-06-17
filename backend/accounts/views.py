from django.contrib.auth import login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class GetCSRFToken(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, format=None):
        return Response({'sucesso': 'Cookie csrf configurado'})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        usuario = getattr(user, 'usuario', None)

        return Response(
            {
                'message': 'Login realizado com sucesso.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'usuario_id': usuario.id if usuario else None,
                    'eh_admin': usuario.eh_admin if usuario else False,
                },
            },
            status=status.HTTP_200_OK,
        )


import math
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action

def get_lmsr_cost(q_sucesso, q_fracasso, b):
    # C = b * ln(e^(q_sucesso/b) + e^(q_fracasso/b))
    # to avoid overflow, use log-sum-exp trick:
    # ln(e^x + e^y) = max(x, y) + ln(e^(x - max(x,y)) + e^(y - max(x,y)))
    b = float(b)
    q_s = float(q_sucesso)
    q_f = float(q_fracasso)
    
    x = q_s / b
    y = q_f / b
    max_val = max(x, y)
    
    return b * (max_val + math.log(math.exp(x - max_val) + math.exp(y - max_val)))

def get_lmsr_prices(q_sucesso, q_fracasso, b):
    b = float(b)
    q_s = float(q_sucesso)
    q_f = float(q_fracasso)
    
    x = q_s / b
    y = q_f / b
    max_val = max(x, y)
    
    denom = math.exp(x - max_val) + math.exp(y - max_val)
    p_sucesso = math.exp(x - max_val) / denom
    p_fracasso = math.exp(y - max_val) / denom
    return p_sucesso, p_fracasso


class ComentarioViewSet(ModelViewSet):
    queryset = Comentario.objects.all().order_by('-criado_em')
    serializer_class = ComentarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mercado']


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class MercadoViewSet(ModelViewSet):
    queryset = Mercado.objects.all()
    serializer_class = MercadoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categorias']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_encerramento', 'liquidez_inicial']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def check_permissions(self, request):
        super().check_permissions(request)
        # RN02: Apenas administradores podem cadastrar mercados de previsão
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            usuario = getattr(request.user, 'usuario', None)
            if not usuario or not usuario.eh_admin:
                self.permission_denied(request, message="Somente administradores podem criar ou gerenciar mercados.")


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comprar(self, request, pk=None):
        mercado = self.get_object()
        if not mercado.ativo:
            return Response({'error': 'Mercado encerrado não permite novas operações.'}, status=status.HTTP_400_BAD_REQUEST)

        # check if it is past end date
        if mercado.data_encerramento < timezone.now().date():
            return Response({'error': 'Mercado com data de encerramento ultrapassada.'}, status=status.HTTP_400_BAD_REQUEST)

        eh_sucesso = request.data.get('eh_sucesso')
        quantidade = request.data.get('quantidade')

        if eh_sucesso is None or quantidade is None:
            return Response({'error': 'eh_sucesso e quantidade são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError()
        except ValueError:
            return Response({'error': 'Quantidade deve ser um inteiro positivo.'}, status=status.HTTP_400_BAD_REQUEST)

        eh_sucesso = bool(eh_sucesso)
        usuario = request.user.usuario

        with transaction.atomic():
            # locking row
            usuario = Usuario.objects.select_for_update().get(id=usuario.id)
            mercado = Mercado.objects.select_for_update().get(id=mercado.id)

            q_s = float(mercado.valor_total_sucesso)
            q_f = float(mercado.valor_total_fracasso)
            b = float(mercado.liquidez_inicial)

            cost_before = get_lmsr_cost(q_s, q_f, b)
            if eh_sucesso:
                cost_after = get_lmsr_cost(q_s + quantidade, q_f, b)
            else:
                cost_after = get_lmsr_cost(q_s, q_f + quantidade, b)

            valor_total = cost_after - cost_before

            if float(usuario.saldo) < valor_total:
                return Response({'error': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update prices dynamically post-trade
            if eh_sucesso:
                mercado.valor_total_sucesso = float(mercado.valor_total_sucesso) + quantidade
            else:
                mercado.valor_total_fracasso = float(mercado.valor_total_fracasso) + quantidade
            
            p_s, p_f = get_lmsr_prices(mercado.valor_total_sucesso, mercado.valor_total_fracasso, b)
            preco_medio_op = valor_total / quantidade

            # Update User Balance
            usuario.saldo = float(usuario.saldo) - valor_total
            usuario.save()

            # Record Operacao
            operacao = Operacao.objects.create(
                tipo=Operacao.TipoOperacao.COMPRA,
                quantidade=quantidade,
                preco_medio=preco_medio_op,
                valor_total=valor_total,
                mercado=mercado,
                usuario=usuario
            )

            # Update/Create Acao (position)
            acao, created = Acao.objects.get_or_create(
                usuario=usuario,
                mercado=mercado,
                eh_sucesso=eh_sucesso,
                defaults={'quantidade': 0, 'preco_medio': 0}
            )

            # Recalculate average price
            # Preço Médio = ((Quantidade Atual * Preço Médio Atual) + (Quantidade Comprada * Preço Médio da Operação)) / (Quantidade Atual + Quantidade Comprada)
            q_atual = acao.quantidade
            pm_atual = float(acao.preco_medio)
            novo_pm = ((q_atual * pm_atual) + (quantidade * preco_medio_op)) / (q_atual + quantidade)
            
            acao.quantidade = q_atual + quantidade
            acao.preco_medio = novo_pm
            acao.save()

            mercado.save()

            # Register HistoricoMercado
            HistoricoMercado.objects.create(
                data_hora=timezone.now(),
                percentual_sucesso=p_s,
                percentual_fracasso=p_f,
                mercado=mercado
            )

        return Response(MercadoSerializer(mercado).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vender(self, request, pk=None):
        mercado = self.get_object()
        if not mercado.ativo:
            return Response({'error': 'Mercado encerrado não permite novas operações.'}, status=status.HTTP_400_BAD_REQUEST)

        eh_sucesso = request.data.get('eh_sucesso')
        quantidade = request.data.get('quantidade')

        if eh_sucesso is None or quantidade is None:
            return Response({'error': 'eh_sucesso e quantidade são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError()
        except ValueError:
            return Response({'error': 'Quantidade deve ser um inteiro positivo.'}, status=status.HTTP_400_BAD_REQUEST)

        eh_sucesso = bool(eh_sucesso)
        usuario = request.user.usuario

        with transaction.atomic():
            usuario = Usuario.objects.select_for_update().get(id=usuario.id)
            mercado = Mercado.objects.select_for_update().get(id=mercado.id)

            # Get user position
            try:
                acao = Acao.objects.select_for_update().get(usuario=usuario, mercado=mercado, eh_sucesso=eh_sucesso)
            except Acao.DoesNotExist:
                return Response({'error': 'Você não possui ações deste tipo neste mercado.'}, status=status.HTTP_400_BAD_REQUEST)

            if acao.quantidade < quantidade:
                return Response({'error': 'Quantidade de ações insuficiente para venda.'}, status=status.HTTP_400_BAD_REQUEST)

            q_s = float(mercado.valor_total_sucesso)
            q_f = float(mercado.valor_total_fracasso)
            b = float(mercado.liquidez_inicial)

            cost_before = get_lmsr_cost(q_s, q_f, b)
            if eh_sucesso:
                cost_after = get_lmsr_cost(q_s - quantidade, q_f, b)
            else:
                cost_after = get_lmsr_cost(q_s, q_f - quantidade, b)

            valor_total = cost_before - cost_after  # Revenue received by user

            # Update Market State
            if eh_sucesso:
                mercado.valor_total_sucesso = float(mercado.valor_total_sucesso) - quantidade
            else:
                mercado.valor_total_fracasso = float(mercado.valor_total_fracasso) - quantidade

            p_s, p_f = get_lmsr_prices(mercado.valor_total_sucesso, mercado.valor_total_fracasso, b)
            preco_medio_op = valor_total / quantidade

            # Update User Balance
            usuario.saldo = float(usuario.saldo) + valor_total
            usuario.save()

            # Record Operacao
            Operacao.objects.create(
                tipo=Operacao.TipoOperacao.VENDA,
                quantidade=quantidade,
                preco_medio=preco_medio_op,
                valor_total=valor_total,
                mercado=mercado,
                usuario=usuario
            )

            # Update user position
            acao.quantidade = acao.quantidade - quantidade
            if acao.quantidade == 0:
                acao.delete()
            else:
                # Average price doesn't change on selling shares, we just reduce the count.
                # Standard practice is keeping the purchase price average.
                acao.save()

            mercado.save()

            # Register HistoricoMercado
            HistoricoMercado.objects.create(
                data_hora=timezone.now(),
                percentual_sucesso=p_s,
                percentual_fracasso=p_f,
                mercado=mercado
            )

        return Response(MercadoSerializer(mercado).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def encerrar(self, request, pk=None):
        mercado = self.get_object()
        
        # Check if the user is an admin
        if not request.user.usuario.eh_admin:
            return Response({'error': 'Somente administradores podem encerrar mercados.'}, status=status.HTTP_403_FORBIDDEN)

        if not mercado.ativo:
            return Response({'error': 'Mercado já foi encerrado.'}, status=status.HTTP_400_BAD_REQUEST)

        sucesso = request.data.get('sucesso')
        if sucesso is None:
            return Response({'error': 'O campo sucesso é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        sucesso = bool(sucesso)

        with transaction.atomic():
            mercado = Mercado.objects.select_for_update().get(id=mercado.id)
            mercado.ativo = False
            mercado.save()

            # Register resolution
            Resultado.objects.create(
                sucesso=sucesso,
                mercado=mercado,
                usuario=request.user.usuario
            )

            # Find all winning positions
            # Liquidate positions: each winning share is bought/redeemed for R$1.00.
            acoes_vencedoras = Acao.objects.filter(mercado=mercado, eh_sucesso=sucesso)
            for acao in acoes_vencedoras:
                usuario_ganhador = Usuario.objects.select_for_update().get(id=acao.usuario.id)
                ganho = acao.quantidade * 1.00
                usuario_ganhador.saldo = float(usuario_ganhador.saldo) + ganho
                usuario_ganhador.save()

                # Register the payout as a specialized Venda operacao or simple payout log.
                # We can just delete their assets since they were resolved.
                acao.delete()

            # Clean up losing assets for this market
            Acao.objects.filter(mercado=mercado).delete()

        return Response({'message': 'Mercado encerrado com sucesso.'}, status=status.HTTP_200_OK)


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [SessionAuthentication]

    def get_permissions(self):
        permission_classes = [AllowAny] if self.action == 'create' else [IsAuthenticated]
        return [permission() for permission in permission_classes]


class AcaoViewSet(ModelViewSet):
    queryset = Acao.objects.all()
    serializer_class = AcaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user.usuario)



