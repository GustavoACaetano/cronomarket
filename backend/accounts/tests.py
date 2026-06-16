from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Mercado, Usuario, Categoria, Acao, Operacao, Resultado, HistoricoMercado
import datetime

class CronomarketTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user_data = {
            'username': 'lucas',
            'email': 'lucas@gmail.com',
            'password': 'password123'
        }
        # Create user via serializer/view to verify starting balance
        url = reverse('usuario-list')
        response = self.client.post(url, {'dados_usuario': self.user_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user = User.objects.get(username='lucas')
        self.usuario = self.user.usuario

        # Login
        self.client.login(username='lucas', password='password123')

        # Create Categoria
        self.categoria = Categoria.objects.create(nome='Esportes')

        # Create Mercado
        self.mercado = Mercado.objects.create(
            titulo='Brasil campeão da copa?',
            descricao='Será que o Brasil ganha a copa?',
            data_encerramento=timezone.now().date() + datetime.timedelta(days=10),
            regra_encerramento='Verificação oficial da FIFA',
            opcao_sucesso='Sim',
            opcao_fracasso='Não',
            link_imagem='https://exemplo.com/imagem.png',
            ativo=True,
            liquidez_inicial=100.00,
            valor_total_sucesso=0.00,
            valor_total_fracasso=0.00
        )
        self.mercado.categorias.add(self.categoria)

    def test_registration_starting_balance(self):
        # RN14: O sistema deve garantir que todo usuário que se cadastrar receba um saldo inicial de R$300,00
        self.assertEqual(float(self.usuario.saldo), 300.00)

    def test_buy_and_sell_actions(self):
        # Buy success shares
        url = reverse('mercado-comprar', args=[self.mercado.id])
        response = self.client.post(url, {'eh_sucesso': True, 'quantidade': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check balance has decreased (buying success shares increases the cost function)
        self.usuario.refresh_from_db()
        self.assertLess(float(self.usuario.saldo), 300.00)

        # Check Acao exists
        acao = Acao.objects.get(usuario=self.usuario, mercado=self.mercado)
        self.assertEqual(acao.quantidade, 10)
        self.assertTrue(acao.eh_sucesso)

        # Check Operacao is created
        self.assertTrue(Operacao.objects.filter(usuario=self.usuario, mercado=self.mercado, tipo=Operacao.TipoOperacao.COMPRA).exists())

        # Sell success shares
        url_vender = reverse('mercado-vender', args=[self.mercado.id])
        response_vender = self.client.post(url_vender, {'eh_sucesso': True, 'quantidade': 5}, format='json')
        self.assertEqual(response_vender.status_code, status.HTTP_200_OK)

        acao.refresh_from_db()
        self.assertEqual(acao.quantidade, 5)

        # Check balance increased on sell
        new_balance = float(self.usuario.saldo)
        self.assertTrue(Operacao.objects.filter(usuario=self.usuario, mercado=self.mercado, tipo=Operacao.TipoOperacao.VENDA).exists())

    def test_market_closure_and_resolution(self):
        # Make the user an admin
        self.usuario.eh_admin = True
        self.usuario.save()

        # Buy shares first
        url_comprar = reverse('mercado-comprar', args=[self.mercado.id])
        self.client.post(url_comprar, {'eh_sucesso': True, 'quantidade': 10}, format='json')

        self.usuario.refresh_from_db()
        balance_before_close = float(self.usuario.saldo)

        # Close market
        url_encerrar = reverse('mercado-encerrar', args=[self.mercado.id])
        response = self.client.post(url_encerrar, {'sucesso': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mercado.refresh_from_db()
        self.assertFalse(self.mercado.ativo)

        # Check resolution Resultado object
        self.assertTrue(Resultado.objects.filter(mercado=self.mercado, sucesso=True).exists())

        # Payout should be R$1.00 per share: we had 10 shares, so we get R$10.00
        self.usuario.refresh_from_db()
        self.assertAlmostEqual(float(self.usuario.saldo), balance_before_close + 10.00)

        # Asset should be deleted after liquidation
        self.assertFalse(Acao.objects.filter(usuario=self.usuario, mercado=self.mercado).exists())
