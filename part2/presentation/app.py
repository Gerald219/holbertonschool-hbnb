from flask import Flask
from flask_restx import Api
from presentation.users import api as users_ns

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='API',
    description='User API'
)

# Register namespaces
api.add_namespace(users_ns, path='/users')


if __name__ == '__main__':
    app.run(debug=True)
