
import os 
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

# Instancia as extensões
db = SQLAlchemy()
migrate = Migrate()
session = Session()

def create_app(config_class=Config):
    """A fábrica de aplicação."""
    
    # Cria a instância principal do Flask
    app = Flask(__name__, static_url_path='/noticias/static')
    
    # Carrega as configurações
    app.config.from_object(config_class)

    # Define o caminho completo para a pasta de uploads
    upload_path = os.path.join(app.root_path, 'static/uploads')
    app.config['UPLOAD_FOLDER'] = upload_path
    
    # Garante que a pasta de uploads exista
    os.makedirs(upload_path, exist_ok=True)

    # Conecta as extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Registra os Blueprints (rotas/views)
    with app.app_context():
        # Importa os modelos
        from . import models

        # Registra a nova rota
        from . import routes
        # O Traefik manda /noticias/*, e remove o /noticias.
        # Então, o Flask vê apenas / e /criar
        app.register_blueprint(routes.bp, url_prefix='/noticias')

        # Cria as tabelas do banco
        db.create_all()

    return app