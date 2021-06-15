from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_limiter.util import get_remote_address
from flask_apispec import MethodResource, doc, use_kwargs
from marshmallow import Schema
from marshmallow.fields import String, Integer
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='REST API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
docs = FlaskApiSpec(app)

images = {}

image_post_args = reqparse.RequestParser()
image_post_args.add_argument("nombre", type = str, help = "El nombre de la imagen es obligatorio", required = True)
image_post_args.add_argument("formato", type = str, help = "El formato de la imagen es obligatorio", required = True)
image_post_args.add_argument("size", type = int, help = "El tamaño de la imagen es obligatorio", required = True)

resource_fields = {
	'id': fields.Integer,
	'nombre': fields.String,
	'formato': fields.String,
	'size': fields.Integer
}

def abort_if_image_exist(image_id):
    if image_id in images:
        abort(409, message = "Imagen existente") 
def abort_if_image_does_not_exist(image_id):
    if image_id not in images:
        abort(404, message = "No se pudo encontrar la imagen")

class ImagesModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    formato = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Image(nombre={nombre}, formato={formato}, size={size})"

#db.create_all()

class BodySchema(Schema):

    id = Integer()
    nombre = String()
    formato = String()
    size = Integer()


class Images(MethodResource, Resource):

    @doc(description='Método GET HTTP en mi API.', tags=['Images'])
    @marshal_with(resource_fields)
    def get(self, image_id):
        '''Método GET
        abort_if_image_does_not_exist(image_id)
        return images[image_id]'''
        result = ImagesModel.query.filter_by(id=image_id).first()
        if not result:
            abort(404, message="No se encontró una imagen con ese id")
        return result

    @doc(description='Método POST HTTP en mi API.', tags=['Images'])
    @use_kwargs(BodySchema)
    @marshal_with(resource_fields)
    def post(self, image_id, **kwargs):
        '''Método POST
        abort_if_image_exist(image_id)
        args = image_post_args.parse_args()
        images[image_id] = args
        return images[image_id], 201'''
        args = image_post_args.parse_args()
        result = ImagesModel.query.filter_by(id=image_id).first()
        if result:
            abort(409, message="Ya hay una imagen con ese id...")
        imagen = ImagesModel(id=image_id, nombre=args['nombre'], formato=args['formato'], size=args['size'])
        db.session.add(imagen)
        db.session.commit()
        return imagen, 201

    @doc(description='Método DELETE HTTP en mi API.', tags=['Images'])
    def delete(self, image_id):
        '''Método DELETE
        abort_if_image_does_not_exist(image_id)
        del images[image_id]
        return '', 204'''
        result = ImagesModel.query.filter_by(id=image_id).first()
        if not result:
            abort(404, message = 'No existe la imagen')
        db.session.delete(result)
        db.session.commit()
        return {'message':'Imagen borrada'}, 204


api.add_resource(Images, '/images/<int:image_id>')
docs.register(Images)

if __name__ == "__main__":
    app.run(debug=True)