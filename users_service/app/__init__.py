

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_bcrypt import Bcrypt
from prometheus_flask_exporter import PrometheusMetrics

# Instancia as extensões
db = SQLAlchemy()
migrate = Migrate()
session = Session()
bcrypt = Bcrypt()
metrics = PrometheusMetrics.for_app_factory()

def create_app(config_class=Config):
    """A fábrica de aplicação."""

    # Cria a instância principal do Flask
    app = Flask(__name__)

    # Carrega as configurações do config.py
    app.config.from_object(config_class)

    # Conecta as extensões com a instância do app
    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    bcrypt.init_app(app)
    metrics.init_app(app)

    # Registra os Blueprints (rotas/views)
    with app.app_context():
        # Importa os modelos 
        from . import models
        
        # Importa e registra as rotas
        # Traefik remove '/cadastro' e '/api' via StripPrefix middleware
        from . import auth_routes
        from . import api_routes
        
        app.register_blueprint(auth_routes.bp, url_prefix='/cadastro')
        app.register_blueprint(api_routes.bp, url_prefix='/api')
        
        # Cria as tabelas do banco 
        db.create_all()

    @app.route('/')
    def root_redirect():
        from flask import redirect
        return redirect('/cadastro/login')

    @app.route('/health')
    def health_check():
        return {'status': 'ok'}, 200

    return app

    