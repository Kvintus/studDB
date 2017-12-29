from flask_restplus import Api

from studentsNamespace import students_api

api = Api(
    title='StudDB REST API',
    version='1.0',
    description='Rest api',
    # All API metadatas
)

api.add_namespace(students_api, url_prefix="/api/student")
