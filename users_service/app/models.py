
from . import db, bcrypt  # do __init__.py

class User(db.Model):
    """
    Define a tabela 'user' no banco de dados.
    """
    __tablename__ = 'user' 
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # armazena a senha como um hash, não texto puro
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """
        Gera um hash para a senha e o armazena.
        Substituto do 'set_password' do Django.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Verifica se a senha fornecida bate com o hash armazenado.
        Substituto do 'check_password' do Django.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        # facilita o debug
        return f'<User {self.username}>'