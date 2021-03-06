from flask_restplus import Api
from flask import Blueprint

from .studentsNamespace import students_api
from .parentsNamespace import parents_api
from .professorsNamespace import professors_api
from .classesNamespace import classes_api



authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

apiBlueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(apiBlueprint,
    title='StudDB REST API',
    version='1.0',
    name='Peter',
    description='Rest api',
    authorizations=authorizations
)

api.add_namespace(students_api, path="/student")
api.add_namespace(parents_api, path="/parent")
api.add_namespace(professors_api, path="/professor")
api.add_namespace(classes_api, path="/class")
