import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Articulo


class ArticuloTestCase(TestCase):
    """Casos de prueba para el modelo Articulo."""

    def setUp(self) -> None:
        """Este método se ejecuta antes de cada prueba para crear algunos
        artículos de prueba."""

        # Crear un usuario y autenticarse
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)

        Articulo.objects.create(
            referencia="ART123",
            nombre="Artículo 1",
            descripcion="Descripción 1",
            precio_sin_impuestos=100,
            impuesto_aplicable=21
        )
        Articulo.objects.create(
            referencia="ART124",
            nombre="Artículo 2",
            descripcion="Descripción 2",
            precio_sin_impuestos=200,
            impuesto_aplicable=10
        )

    def test_crear_articulo(self) -> None:
        """Prueba que se pueda crear un artículo exitosamente."""
        response = self.client.post(
            reverse('crear_articulo'),
            data=json.dumps({
                'referencia': 'ART125',
                'nombre': 'Artículo 3',
                'descripcion': 'Descripción 3',
                'precio_sin_impuestos': 150,
                'impuesto_aplicable': 18
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Articulo.objects.count(), 3)

    def test_listar_articulos(self) -> None:
        """Prueba que se puedan listar todos los artículos."""
        response = self.client.get(reverse('listar_articulos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_obtener_articulo(self) -> None:
        """Prueba que se pueda obtener un artículo por su ID."""
        articulo = Articulo.objects.first()
        response = self.client.get(reverse('detalle_articulo',
                                           args=[articulo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nombre'], articulo.nombre)

    def test_editar_articulo(self) -> None:
        """Prueba que se pueda editar un artículo por su ID."""
        articulo = Articulo.objects.first()
        response = self.client.put(
            reverse('detalle_articulo', args=[articulo.id]),
            data=json.dumps({
                'referencia': 'ART126',
                'nombre': 'Artículo Editado',
                'descripcion': 'Descripción Editada',
                'precio_sin_impuestos': 180,
                'impuesto_aplicable': 15
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        articulo.refresh_from_db()
        self.assertEqual(articulo.nombre, 'Artículo Editado')

    def test_articulo_no_existente(self) -> None:
        "Prueba que la solicitud de un artículo no existente retorne un 404."
        response = self.client.get(reverse('detalle_articulo', args=[999]))
        self.assertEqual(response.status_code, 404)
