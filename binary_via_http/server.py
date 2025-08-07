import flask
from flask_restx import Api, Resource
import requests

bills = flask.Blueprint("bills", __name__)

api = Api(
    bills,
    title="Services API",
    description="API para la gestión de facturas",
)

#recibir un archivo binario
class Upload(Resource):
    def post(self):
        if "file" not in flask.request.files:
            return "No file part in request", 400
        file = flask.request.files["file"]
        if file.filename == "":
            return "Nombre vacio", 400
        contenido = file.read()
        LOGGER.info(f"Nombre del archivo: {file.filename}")
        LOGGER.info(f"Contenido del archivo: {contenido}")
        peso = len(contenido)

        return f"Archivo {file.filename} subido correctamente. Peso: {peso} bytes", 200


api.add_resource(Upload, '/upload') 
