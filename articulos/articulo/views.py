import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import Articulo


class ArticuloCreateView(APIView):
    """Vista para crear un nuevo artículo."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> JsonResponse:
        """Crea un nuevo artículo en la base de datos."""

        data = json.loads(request.body)

        # Validar los datos del artículo
        if (not data['referencia']
            or not data['nombre']
            or not data['descripcion']
            or not data['precio_sin_impuestos']
                or not data['impuesto_aplicable']):
            return JsonResponse({'error': 'Todos los campos son obligatorios'},
                                status=status.HTTP_400_BAD_REQUEST)

        if (data['precio_sin_impuestos'] <= 0
                or data['impuesto_aplicable'] <= 0):
            return JsonResponse(
                {'error': 'El precio y el impuesto deben ser mayores que 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        articulo = Articulo.objects.create(
            referencia=data['referencia'],
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio_sin_impuestos=data['precio_sin_impuestos'],
            impuesto_aplicable=data['impuesto_aplicable']
        )
        return JsonResponse(model_to_dict(articulo),
                            status=status.HTTP_201_CREATED)


class ArticuloDetailView(APIView):
    """Vista para obtener un artículo por su ID."""

    permission_classes = [IsAuthenticated]

    def get(self, request, id) -> JsonResponse:
        """Obtiene el detalle de un artículo."""

        articulo = get_object_or_404(Articulo, id=id)
        return JsonResponse(model_to_dict(articulo))

    def put(self, request, id) -> JsonResponse:
        """Actualiza los datos de un artículo."""

        data = json.loads(request.body)
        articulo = get_object_or_404(Articulo, id=id)
        articulo.referencia = data['referencia']
        articulo.nombre = data['nombre']
        articulo.descripcion = data['descripcion']
        articulo.precio_sin_impuestos = data['precio_sin_impuestos']
        articulo.impuesto_aplicable = data['impuesto_aplicable']
        articulo.save()
        return JsonResponse(model_to_dict(articulo), status=status.HTTP_200_OK)


class ArticuloListView(APIView):
    """Vista para obtener todos los artículos."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> JsonResponse:
        """Obtiene todos los artículos."""
        articulos = Articulo.objects.all()
        articulos_json = list(articulos.values())
        return JsonResponse(articulos_json, safe=False)
