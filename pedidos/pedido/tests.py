import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Pedido, DetallePedido


class PedidoTestCase(TestCase):
    """Casos de prueba para el modelo Pedido."""

    def setUp(self) -> None:
        """Configura un usuario y autentica el cliente de prueba."""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)

    @patch('pedido.views.requests.get')
    def test_crear_pedido_exitoso(self, mock_get) -> None:
        """Prueba la creación de un pedido con artículos válidos."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'referencia': 'ART123',
            'nombre': 'Artículo 1',
            'precio_sin_impuestos': 100,
            'impuesto_aplicable': 21,
            'descripcion': 'Descripción del artículo 1'
        }

        response = self.client.post(reverse('crear_pedido'), json.dumps({
            'articulos': [
                {'id': 1, 'cantidad': 2}
            ]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        pedido = Pedido.objects.get()
        self.assertEqual(float(pedido.precio_total_sin_impuestos), 200.00)
        self.assertEqual(float(pedido.precio_total_con_impuestos), 242.00)

    @patch('pedido.views.requests.get')
    def test_crear_pedido_articulo_inexistente(self, mock_get) -> None:
        """Prueba la creación de un pedido con un artículo inexistente."""
        mock_get.return_value.status_code = 404

        response = self.client.post(reverse('crear_pedido'), json.dumps({
            'articulos': [
                {'id': 999, 'cantidad': 1}
            ]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Pedido.objects.count(), 0)

    @patch('pedido.views.requests.get')
    def test_crear_pedido_cantidad_negativa(self, mock_get) -> None:
        """Prueba la creación de un pedido con una cantidad negativa."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'referencia': 'ART123',
            'nombre': 'Artículo 1',
            'precio_sin_impuestos': 100,
            'impuesto_aplicable': 21
        }

        response = self.client.post(reverse('crear_pedido'), json.dumps({
            'articulos': [
                {'id': 1, 'cantidad': -2}
            ]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_crear_pedido_sin_articulos(self) -> None:
        """Prueba la creación de un pedido sin artículos."""
        response = self.client.post(reverse('crear_pedido'), json.dumps({
            'articulos': []
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)


class PedidoEditTestCase(TestCase):
    """Casos de prueba para la edición de un pedido."""

    def setUp(self) -> None:
        """Configura un pedido inicial para editarlo."""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)

        self.pedido = Pedido.objects.create()
        DetallePedido.objects.create(
            pedido=self.pedido,
            articulo_id=1,
            articulo_referencia="ART123",
            articulo_nombre="Artículo 1",
            articulo_precio_sin_impuestos=100,
            articulo_impuesto_aplicable=21,
            cantidad=2
        )
        self.pedido.calcular_precio_total()

    @patch('pedido.views.requests.get')
    def test_editar_pedido(self, mock_get) -> None:
        """Prueba la edición de un pedido existente."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'referencia': 'ART124',
            'nombre': 'Artículo 2',
            'precio_sin_impuestos': 200,
            'impuesto_aplicable': 10,
            'descripcion': 'Descripción del artículo 2'
        }

        response = self.client.put(
            reverse('editar_pedido', args=[self.pedido.id]),
            json.dumps({
                'articulos': [
                    {'id': 1, 'cantidad': 1}
                ]
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.precio_total_sin_impuestos, 200)
        self.assertEqual(self.pedido.precio_total_con_impuestos, 220)

    @patch('pedido.views.requests.get')
    def test_editar_pedido_articulo_inexistente(self, mock_get) -> None:
        """Prueba la edición de un pedido con un artículo inexistente."""
        mock_get.return_value.status_code = 404

        response = self.client.put(
            reverse('editar_pedido', args=[self.pedido.id]),
            json.dumps({
                'articulos': [
                    {'id': 999, 'cantidad': 1}
                ]
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.precio_total_sin_impuestos, 200)


class PedidoDetailTestCase(TestCase):
    """Casos de prueba para la obtención de un pedido."""

    def setUp(self) -> None:
        """Configura un pedido inicial para obtenerlo."""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)

        self.pedido = Pedido.objects.create()
        DetallePedido.objects.create(
            pedido=self.pedido,
            articulo_id=1,
            articulo_referencia="ART123",
            articulo_nombre="Artículo 1",
            articulo_precio_sin_impuestos=100,
            articulo_impuesto_aplicable=21,
            cantidad=2
        )
        self.pedido.calcular_precio_total()

    def test_obtener_pedido(self) -> None:
        """Prueba obtener un pedido existente por su ID."""
        response = self.client.get(
            reverse('detalle_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            float(response.json()['precio_total_sin_impuestos']), 200.00)
        self.assertEqual(
            float(response.json()['precio_total_con_impuestos']), 242.00)

    def test_obtener_pedido_inexistente(self) -> None:
        """Prueba obtener un pedido inexistente."""
        response = self.client.get(reverse('detalle_pedido', args=[999]))
        self.assertEqual(response.status_code, 404)


class PedidoListTestCase(TestCase):
    """Casos de prueba para la lista de pedidos."""

    def setUp(self) -> None:
        """Configura varios pedidos para listarlos."""
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)

        self.pedido1 = Pedido.objects.create()
        DetallePedido.objects.create(
            pedido=self.pedido1,
            articulo_id=1,
            articulo_referencia="ART123",
            articulo_nombre="Artículo 1",
            articulo_precio_sin_impuestos=100,
            articulo_impuesto_aplicable=21,
            cantidad=2
        )
        self.pedido1.calcular_precio_total()

        self.pedido2 = Pedido.objects.create()
        DetallePedido.objects.create(
            pedido=self.pedido2,
            articulo_id=2,
            articulo_referencia="ART124",
            articulo_nombre="Artículo 2",
            articulo_precio_sin_impuestos=200,
            articulo_impuesto_aplicable=10,
            cantidad=1
        )
        self.pedido2.calcular_precio_total()

    def test_listar_pedidos(self) -> None:
        """Prueba listar todos los pedidos."""
        response = self.client.get(reverse('listar_pedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
