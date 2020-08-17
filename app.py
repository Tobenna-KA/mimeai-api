from flask import Flask
from flasgger import Swagger
from api.route.home import home_api

app = Flask(__name__)


def create_app():
    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    swagger = Swagger(app)

    app.register_blueprint(home_api, url_prefix='/api')

    return app


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Origin', 'GET,PUT,POST,DELETE')

    return response


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
