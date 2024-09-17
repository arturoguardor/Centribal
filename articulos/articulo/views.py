from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Articulo
from django.forms.models import model_to_dict
import json


class ArticuloCreateView(APIView):
    """Vista para crear un nuevo artículo."""

    permission_classes = [IsAuthenticated]

    def post(self, request) -> JsonResponse:
        """Crea un nuevo artículo en la base de datos."""

        data = json.loads(request.body)
        articulo = Articulo.objects.create(
            referencia=data['referencia'],
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            precio_sin_impuestos=data['precio_sin_impuestos'],
            impuesto_aplicable=data['impuesto_aplicable']
        )
        return JsonResponse(model_to_dict(articulo), status=201)


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
        return JsonResponse(model_to_dict(articulo), status=200)


class ArticuloListView(APIView):
    """Vista para obtener todos los artículos."""

    permission_classes = [IsAuthenticated]

    def get(self, request) -> JsonResponse:
        """Obtiene todos los artículos."""
        articulos = Articulo.objects.all()
        articulos_json = list(articulos.values())
        return JsonResponse(articulos_json, safe=False)
