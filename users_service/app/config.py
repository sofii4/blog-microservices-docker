
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

    # Flask-Session configuration with Redis
    SESSION_TYPE = os.environ.get('SESSION_TYPE') 
    SESSION_REDIS = redis.from_url(os.environ.get('SESSION_REDIS'))
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True