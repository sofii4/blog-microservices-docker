
import os
import redis 

class Config:
    """Load application configuration from environment variables."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set. Aborting.")

    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,      # testa conexão antes de usar
    "pool_recycle": 280,        # recicla conexões a cada 280s (antes do MySQL fechar em 300s)
    "pool_timeout": 20,         # timeout para obter conexão do pool
}

    # Flask-Session configuration with Redis
    SESSION_TYPE = os.environ.get('SESSION_TYPE') 
    SESSION_REDIS_URL_VALUE = os.environ.get('SESSION_REDIS_URL') or os.environ.get('SESSION_REDIS')
    if not SESSION_REDIS_URL_VALUE:
        raise ValueError("Nenhuma variável SESSION_REDIS ou SESSION_REDIS_URL definida.")
    SESSION_REDIS = redis.from_url(SESSION_REDIS_URL_VALUE)
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True