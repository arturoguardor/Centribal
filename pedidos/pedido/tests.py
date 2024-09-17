from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .models import Pedido, DetallePedido


class PedidoTestCase(TestCase):
    """Casos de prueba para el modelo Pedido.

    :param TestCase: Clase base para pruebas unitarias en Django
    :type TestCase: clase
    """

    @patch('app.views.requests.get')
    def test_crear_pedido_exitoso(self, mock_get) -> None:
        """Prueba la creación de un pedido con artículos válidos.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 10,
            'referencia': 'ART123',
            'nombre': 'Artículo 10',
            'precio_sin_impuestos': 100,
            'impuesto_aplicable': 21
        }

        response = self.client.post(reverse('crear_pedido'), {
            'articulos': [
                {'id': 10, 'cantidad': 2}
            ]
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        pedido = Pedido.objects.first()
        self.assertEqual(pedido.precio_total_sin_impuestos, 200)
        self.assertEqual(pedido.precio_total_con_impuestos, 242)

    @patch('app.views.requests.get')
    def test_crear_pedido_articulo_inexistente(self, mock_get) -> None:
        """Prueba la creación de un pedido con un artículo inexistente.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        mock_get.return_value.status_code = 404

        response = self.client.post(reverse('crear_pedido'), {
            'articulos': [
                {'articulo_id': 999, 'cantidad': 1}
            ]
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Pedido.objects.count(), 0)

    @patch('app.views.requests.get')
    def test_crear_pedido_cantidad_negativa(self, mock_get) -> None:
        """Prueba la creación de un pedido con una cantidad negativa.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'referencia': 'ART123',
            'nombre': 'Artículo 1',
            'precio_sin_impuestos': 100,
            'impuesto_aplicable': 21
        }

        response = self.client.post(reverse('crear_pedido'), {
            'articulos': [
                {'articulo_id': 1, 'cantidad': -2}
            ]
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_crear_pedido_sin_articulos(self) -> None:
        """Prueba la creación de un pedido sin artículos.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        response = self.client.post(reverse('crear_pedido'), {
            'articulos': []
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Pedido.objects.count(), 0)


class PedidoEditTestCase(TestCase):
    """Casos de prueba para la edición de un pedido.

    :param TestCase: Clase base para pruebas unitarias en Django
    :type TestCase: clase
    """

    def setUp(self) -> None:
        """Configura un pedido inicial para editarlo.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

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

    @patch('app.views.requests.get')
    def test_editar_pedido(self, mock_get) -> None:
        """Prueba la edición de un pedido existente.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'referencia': 'ART124',
            'nombre': 'Artículo 2',
            'precio_sin_impuestos': 200,
            'impuesto_aplicable': 10
        }

        response = self.client.put(reverse('editar_pedido',
                                           args=[self.pedido.id]), {
            'articulos': [
                {'articulo_id': 1, 'cantidad': 1}
            ]
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.precio_total_sin_impuestos, 200)
        self.assertEqual(self.pedido.precio_total_con_impuestos, 220)

    @patch('app.views.requests.get')
    def test_editar_pedido_articulo_inexistente(self, mock_get) -> None:
        """Prueba la edición de un pedido con un artículo inexistente.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        mock_get.return_value.status_code = 404

        response = self.client.put(reverse('editar_pedido',
                                           args=[self.pedido.id]), {
            'articulos': [
                {'articulo_id': 999, 'cantidad': 1}
            ]
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.precio_total_sin_impuestos, 200)


class PedidoDetailTestCase(TestCase):
    """Casos de prueba para la obtención de un pedido.

    :param TestCase: Clase base para pruebas unitarias en Django
    :type TestCase: clase
    """

    def setUp(self) -> None:
        """Configura un pedido inicial para obtenerlo.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

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
        """Prueba obtener un pedido existente por su ID.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        response = self.client.get(reverse('detalle_pedido',
                                           args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['precio_total_sin_impuestos'], 200)
        self.assertEqual(response.json()['precio_total_con_impuestos'], 242)

    def test_obtener_pedido_inexistente(self) -> None:
        """Prueba obtener un pedido inexistente.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        response = self.client.get(reverse('detalle_pedido', args=[999]))
        self.assertEqual(response.status_code, 404)


class PedidoListTestCase(TestCase):
    """Casos de prueba para la lista de pedidos.

    :param TestCase: Clase base para pruebas unitarias en Django
    :type TestCase: clase
    """

    def setUp(self) -> None:
        """Configura varios pedidos para listarlos.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

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
        """Prueba listar todos los pedidos.

        :param mock_get: Mock para simular la respuesta de la API de artículos
        :type mock_get: mock
        """

        response = self.client.get(reverse('listar_pedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
