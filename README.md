# Aprende sobre JSON y cómo usar APIs creando una con Python

> Taller impartido como parte del AI Gaming 2021

El objetivo principal del taller es la programación de una API web hecha con Python para entender el funcionamiento de las API de Microsoft Azure y el formato JSON.

## Installation

Clonar el repositorio
```sh
git clone https://github.com/OscarSantos98/JSON_y_APIs_workshop.git
```

```
cd https://github.com/OscarSantos98/JSON_y_APIs_workshop.git
```

Luego deberá crearse un virtual environment, ya sea virtualenv o conda environment

```
pip install virtualenv
```
```
virtualenv myenv –p <path del intérprete de Python>
```
```
.\myenv\Scripts\activate
```
```
pip install -r requirements.txt
```
## Requisitos

### IDE

- [Visual Studio Code](https://code.visualstudio.com/download)

*Extensión*
- Python

### Dependencias

- Flask
- Flask-restful
- Flask-apispec
- Flask-limiter
- SQLAlchemy

### Suscripción de Azure (opcional)

- [Prueba gratuita](https://azure.microsoft.com/es-mx/free/search/?&ef_id=EAIaIQobChMIoo38pqXc8AIVgozICh2Elw7lEAAYASAAEgL7aPD_BwE:G:s&OCID=AID2100073_SEM_EAIaIQobChMIoo38pqXc8AIVgozICh2Elw7lEAAYASAAEgL7aPD_BwE:G:s&gclid=EAIaIQobChMIoo38pqXc8AIVgozICh2Elw7lEAAYASAAEgL7aPD_BwE)

## Pasos con Flask

1. Crear Hola mundo

2. Añadir limitadores (checar documentación oficial y copiar el código escribiendo lo siguiente al final del código)

```
if __name__ == "__main__":
    app.run(debug=True)
```

## Pasos con Flask restful

1. Importar paquetes y módulos.

```
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
```

2. Instanciar Flask y Api.

```
app = Flask(__name__)
api = Api(app)
```

3. Crear una clase con un método get y heredar de Resource.

```
class AzureStorage(Resource):
    
    def get(self):
        '''Método GET'''
        return {'data':'Hello'}

```

4. Añadir el recurso a la instancia de Api.

```
api.add_resource(Images, '/Storage')
```

5. Realizar una petición GET desde el navegador y desde otro script llamado request.py.

```
import requests

BASE_ENDPOINT = 'http://127.0.0.1:5000'

response = requests.get(BASE_ENDPOINT + '/Storage')
print(response.json())
```

6. Añadir un método POST.

```
def post(self, image_id, **kwargs):
        '''Método POST'''
        pass
```

7. Instanciar RequestParser()

```
image_post_args = reqparse.RequestParser()
```

8. Agregar argumentos

```
image_post_args.add_argument("nombre", type = str, help = "El nombre de la imagen es obligatorio", required = True)
image_post_args.add_argument("formato", type = str, help = "El formato de la imagen es obligatorio", required = True)
image_post_args.add_argument("size", type = int, help = "El tamaño de la imagen es obligatorio", required = True)
```

9. LLamar a parse_args() en el método post

```
def post(self, image_id, **kwargs):
        '''Método POST
        args = image_post_args.parse_args()
        images[image_id] = args
        return images[image_id], 201'''
```

10. Probar el script request.py con lo siguiente

```
import requests

BASE_ENDPOINT = 'http://127.0.0.1:5000'

data = [{"nombre":"oscar","formato":"jpg","size":10},
{"nombre":"juan","formato":"png","size":17},
{"nombre":"pedro","formato":"jpeg","size":14}]

for i in range(len(data)):

    response = requests.post(BASE_ENDPOINT + '/Storage/' + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE_ENDPOINT + '/Storage/2')
print(response.json())
```

> Durante el taller el problema que se tenía fue que la solicitud de request.py no se había modificado y lo hacía incorrecto. El lado del servidor siempre había estado bien.

11. Crear funciones para evitar errores o sobreescribir valores previos.

```
def abort_if_image_exist(image_id):
    if image_id in images:
        abort(409, message = "Imagen existente") 
def abort_if_image_does_not_exist(image_id):
    if image_id not in images:
        abort(404, message = "No se pudo encontrar la imagen")
```

12. Crear método delete, utilizar una de las funciones anteriores y usar palabra reservada del

```
def delete(self, image_id):
        '''Método DELETE'''
        abort_if_image_does_not_exist(image_id)
        del images[image_id]
        return '', 204
```

Si se desea probar con request.py cabe mencionar que como no retorna un diccionario (los cuales son serializables) no se puede usar response.json()

```
response = requests.delete(BASE_ENDPOINT + '/Storage/0')
print(response)
```

### Documentación basada en la definición OpenAPI

13. Añadir documentación

```
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='REST API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI con la que accedes al json que define tu API
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI con la que accedes a la UI de la documentación de tu API 
})
docs = FlaskApiSpec(app)

docs.register(AzureStorage) # debe ir después de tu clase AzureStorage
```

14. Heredar en la clase principal de MethodResource

```
class AzureStorage(MethodResource, Resource):
```

15. Añadir en get, post y delete

```
 @doc(description='Método HTTP en mi API.', tags=['AzureStorage'])
 ```

16. Crear una clase BodySchema que hereda de Schema y usa fields.

 ```
class BodySchema(Schema):

    nombre = fields.String()
    formato = fields.String()
    size = fields.Integer()
 ```

17. Añadir en post

```
@use_kwargs(BodySchema)
```

> Uno de los motivos por lo que no funcionó el POST desde la documentación durante el taller fue que faltó añadir un argumento al método

```
def post(self, image_id, **kwargs):
```

Sin kwargs, regresa un estatus 500.

### Inclusión de una base de datos para evitar el uso de la memoria.

18. Crear base de datos, importando 

```
from flask_sqlalchemy import SQLAlchemy
```

19. Añadir configuración

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
```

20. Instanciar SQLAlchemy

```
db = SQLAlchemy(app)
```

21. Crear modelo

```
class AzureStorageModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    formato = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Imagen(nombre={self.nombre}, formato={self.formato}, size={self.size})"
```

22. Ejecutar una vez db.create_all() la cual debe ir después de la clase AzureStorageModel

23. Correr script y quitar db.create_all() porque de otro modo se estaría sobreescribiendo el archivo database.db en cada ejecución, es decir, solo lo hacemos una vez para crear ese archivo.

23. Reemplazar get
```
result = AzureStorageModel.query.filter_by(id=image_id).first()
if not result:
    abort(404, message="No se encontró una imagen con ese id")
return result
```

24. Reemplazar post

```
args = image_post_args.parse_args()
result = AzureStorageModel.query.filter_by(id=image_id).first()
if result:
    abort(409, message="Ya hay una imagen con ese id...")
imagen = AzureStorageModel(id=image_id, nombre=args['nombre'], formato=args['formato'], size=args['size'])
db.session.add(imagen)
db.session.commit()
return imagen, 201
```

25. Cambiar fields en los paquetes

```
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from marshmallow.fields import String, Integer
```

26. Reemplazar BodySchema

```
class BodySchema(Schema):

    id = Integer()
    nombre = String()
    formato = String()
    size = Integer()
```

27. Crear diccionario

```
resource_fields = {
	'id': fields.Integer,
	'nombre': fields.String,
	'formato': fields.String,
	'size': fields.Integer
}
```

28. Añadir el decorador a get y post

```
@marshal_with(resource_fields)
```

29. Reemplazar delete

```
result = AzureStorageModel.query.filter_by(id=image_id).first()
if not result:
    abort(404, message = 'No existe la imagen')
db.session.delete(result)
db.session.commit()
return {'message':'Imagen borrada'}, 204
```

30. Probar desde documentación

31. Abrir y realizar consultas desde DB Browser for SQLite

## Pasos para publicar API de Python en Azure

1. Abrir el portal de Azure.

2. Crear un grupo de recursos.

3. Crear una aplicación web.

4. Ir al centro de implementación.

5. Conectar con GitHub (autorizar permisos si no se ha hecho antes).

6. Establecer configuración.

7. Guardar.

8. Clic en registros.

9. Clic en el enlace.

10. Probar con el nuevo endpoint.

