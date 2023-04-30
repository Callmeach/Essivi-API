from flask import Flask, render_template
from flask_cors import CORS
from pod.extension import db

from pod.routes.administrateur import admin_bp
from pod.routes.agentCommercial import agent_bp
from pod.routes.client import client_bp
from pod.routes.livraison import livraison_bp
from pod.routes.login import login_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTION')
        return response

    # @app.route('/login', methods=['GET'])
    # def login():
    #     return {'Hello': 'World'}

    db.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(livraison_bp)
    app.register_blueprint(login_bp)

    return app
