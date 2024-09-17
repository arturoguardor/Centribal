"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView
from articulo.views import ArticuloCreateView, ArticuloDetailView, \
    ArticuloListView


schema_view = get_schema_view(
    openapi.Info(
        title="Artículos API",
        default_version='v1',
        description="Documentación de la API para la gestión de artículos",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soporte@centribal.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('articulos', ArticuloCreateView.as_view(), name='crear_articulo'),
    path('articulos/<int:id>', ArticuloDetailView.as_view(),
         name='detalle_articulo'),
    path('articulos/list/', ArticuloListView.as_view(),
         name='listar_articulos'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
