# Django App

Servicio web para un sistema de pedidos

## Especificaciones

El modelo de datos relacional (utilizando la base de datos SQLite) está diseñado para dos tipos de usuario, Cliente y Proveedor.

Bootstrap 5 fue implementado como framework frontend CSS.

#### Operaciones que el Proveedor puede realizar en la aplicación

- Registrarse como nuevo usuario
- Autenticación de Proveedor (login)
- El usuario Proveedor cuenta con rutas protegidas a las que únicamente el Proveedor tiene acceso
- En la página de inicio del Proveedor, hay un botón para crear un nuevo artículo (código, descripción, precio, proveedor que surte)
- Cuando el artículo es creado, el código sirve como PRIMARY KEY (que se utilza para relacionar otras tablas). Además, el ID del usuario Proveedor automáticamente es asignado al artículo
- Cuando el usuario Cliente hace un pedido, el Proveedor puede consultar los detalles del pedido como el nombre de usuario del Cliente, el número de orden (FOREIGN KEY de tabla Orden), fecha del pedido, el artículo solicitado (FOREIGN KEY de tabla Artículo) y la cantidad
- Finalmente, cuando hay un pedido registrado, el Proveedor puede administrar este pedido hacia un Centro de distribución, hacia una sucursal, o hacia una empresa asociada

#### Operaciones que el Cliente puede realizar en la aplicación

- Registrarse como nuevo usuario
- Autenticación de Cliente (login)
- El usuario Cliente cuenta con rutas protegidas a las que únicamente el Cliente tiene acceso
- Si existen artículos publicados por Proveedores, estos aparecen en la página inicial del Cliente.
- El Cliente puede acceder a los detalles del artículo
- El Cliente puede hacer un nuevo pedido del artículo especificando la urgencia, la cantidad de artículos, e indicar hacia donde se hace el pedido para que el Proveedor lo pueda surtir

## Librerías utilizadas

- Django para construir la aplicación
- Django-rest-framework para la REST API
- Pruebas unitarias integradas en Django que utilizan la librería estándar de Python unittest 
- drg-yasg para la documentación Swagger de los servicios web
- Bootstrap para el frontend

## Instrucciones para ejecutar la aplicación localmente

- A través de una línea de comandos, navegar al directorio donde se encuentra este archivo README

- Instalar las dependencias:

```sh
pip install -r requirements.txt
```

- Ejecutar los comandos SQL para crear la base de datos y las tablas:

```sh
python manage.py migrate
```

- Ejecutar el servidor:

```sh
python manage.py runserver
```

- Abrir tu navegador y consultar la siguiente dirección:

```sh
127.0.0.1:8000
```

## Instrucciones para ejecutar la aplicación en Docker

- A través de una línea de comandos, navegar al directorio donde se encuentra este archivo README

- Ejecutar el siguiente comando para crear e iniciar los servicios de esta aplicación:

```sh
docker compose up --build
```

- Abrir tu navegador y consultar la siguiente dirección:

```sh
0.0.0.1:8000
```