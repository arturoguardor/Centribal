# Centribal Microservicios API

Una REST API para una aplicación de gestión de artículos y pedidos.

 Este proyecto consiste en dos microservicios para la gestión de artículos y pedidos, construidos con **Django** y con un acercamiento a la arquitectura **Hexagonal**. Cada microservicio es independiente y utiliza **MySQL** como base de datos, gestionado a través de **Docker**. Los microservicios permiten realizar las operaciones CRUD sobre artículos y pedidos mediante APIs REST.

## Requisitos

Para ejecutar el proyecto, necesitas tener instalado:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Postman](https://www.postman.com/) para pruebas manuales

## Configuración y Ejecución del Proyecto

### 1. Clonar el repositorio

Primero, clona el repositorio del proyecto en tu máquina local:

```bash
git clone https://github.com/arturoguardor/centribal-api.git
cd centribal-api
```

### 2. Configurar las variables de entorno

Asegúrate de que las bases de datos y los servicios se configuran adecuadamente. No se requiere un archivo `.env` en esta configuración básica, ya que los detalles de las bases de datos están en `docker-compose.yml`. Si es necesario, puedes modificarlo para ajustarlo a tus necesidades.

### 3. Iniciar los microservicios

Antes de iniciar los microservicios, asegúrate de que tienes configurado el archivo `.env` con las variables de entorno y credenciales necesarias para la conexión a la base de datos, JWT Authentication y el acceso a las API's de Artículos y Pedidos. Este archivo puedes crearlo con los datos que te he enviado por correo en un archivo `.txt`.

Ahora puedes iniciar ambos microservicios (Artículos y Pedidos) junto con sus bases de datos MySQL, ejecuta el siguiente comando en la raíz del proyecto:

```bash
docker-compose up --build
```

Esto levantará los contenedores de Docker necesarios para los microservicios y las bases de datos. Los servicios estarán disponibles en:

Artículos: [http://localhost:8000](http://localhost:8000)
Pedidos: [http://localhost:8001](http://localhost:8001)

### 4. JWT Autenticación

El proyecto utiliza **JSON Web Tokens (JWT)** para la autenticación. Para acceder a los endpoints protegidos, primero debes obtener un token de acceso.

#### Obtener un Token JWT

Para obtener un token JWT, realiza una solicitud `POST` al endpoint:

- URL: `/api/token/`
- Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Esto devolverá un token de acceso y un token de refresco. El token de acceso se utilizará para autenticar las solicitudes a los endpoints protegidos.

#### Refrescar el Token JWT

El token de acceso tiene una vida limitada, pero puede ser renovado utilizando el token de refresco. Para hacerlo, realiza una solicitud `POST` al endpoint:

- URL: `/api/token/refresh/`
- Body:

```json
{
  "refresh": "your_refresh_token"
}
```

Esto devolverá un nuevo token de acceso.

### 5. Acceso a la API

#### Artículos

Los endpoints de Artículos están disponibles en [http://localhost:8000](http://localhost:8000):

- `POST /articulos/`: Crear un nuevo artículo.
- `GET /articulos/{id}/`: Obtener un artículo por su ID.
- `PUT /articulos/{id}/`: Editar un artículo.
- `GET /articulos/list/`: Listar todos los artículos.

#### Pedidos

Los endpoints de Pedidos están disponibles en [http://localhost:8001](http://localhost:8001):

- `POST /pedidos/`: Crear un nuevo pedido.
- `GET /pedidos/{id}/`: Obtener un pedido por su ID.
- `PUT /pedidos/{id}/editar`: Editar un pedido.
- `GET /pedidos/list/`: Listar todos los pedidos.

### 6. Documentación de la API

#### Swagger UI

La documentación de la API está disponible a través de ***Swagger UI*** y ***Redoc***. Puedes acceder a ella desde tu navegador:

- Artículos:

  - Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
  - Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

- Pedidos:

  - Swagger UI: [http://localhost:8001/swagger/](http://localhost:8001/swagger/)
  - Redoc: [http://localhost:8001/redoc/](http://localhost:8001/redoc/)

### 7. Pruebas Unitarias

Para ejecutar las pruebas unitarias y asegurarte de que todo el sistema funcione correctamente, puedes ejecutar el siguiente comando en cada microservicio:

Para Artículos:

```bash
docker-compose run articulos_service python manage.py test
Para Pedidos:

```bash
docker-compose run pedidos_service python manage.py test
```

Esto ejecutará las pruebas definidas en los archivos tests.py de cada microservicio y mostrará los resultados en la consola.

### 8. Colección de Postman

He creado una colección de Postman que puedes utilizar para probar los endpoints de la API manualmente. La colección está disponible en el archivo postman_collection.json. Para usarla:

1. Abre Postman.
2. Importa el archivo `Centribal API Collection.postman_collection.json`.
3. Ejecuta las peticiones directamente en tu entorno local.

### 9. Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

```bash
centribal-api/
│
├── articulos/
│   ├── articulo/
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── pedidos/
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── pedido/
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
│
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

Cada microservicio tiene su propio directorio con sus respectivos archivos de configuración, código y pruebas. El archivo docker-compose.yml orquesta la ejecución de los contenedores de Docker para ambos servicios.

### Contacto

Si tienes alguna pregunta o encuentras algún problema, por favor contacta al equipo de desarrollo en [soporte@centribal.com](mailto:soporte@centribal.com).
