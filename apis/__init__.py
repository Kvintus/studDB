from flask_restplus import Api

from .studentsNamespace import students_api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    title='StudDB REST API',
    version='1.0',
    name='Peter',
    description='Rest api',
    authorizations=authorizations
)

api.add_namespace(students_api, path="/api/student")
