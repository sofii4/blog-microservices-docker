
import os
import redis 

class Config:
    """Carrega as configurações do app a partir das variáveis de ambiente."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-padrao-fraca-mude-isso')

    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração do Flask-Session para conectar ao Redis
    # Lê as variáveis do docker-compose.yml
    SESSION_TYPE = os.environ.get('SESSION_TYPE') 
    SESSION_REDIS = redis.from_url(os.environ.get('SESSION_REDIS')) # 'redis://redis-sessions:6379/0'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True # Assina o cookie de sessão por segurança