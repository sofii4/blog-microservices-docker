

from . import db  # do __init__.py
from datetime import datetime

class Noticia(db.Model):
    """
    Define a tabela 'noticia' no banco de dados.
    """
    __tablename__ = 'noticia'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    # salva apenas o NOME DO ARQUIVO da imagem.
    imagem = db.Column(db.String(200), nullable=True) 
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # armazena apenas o ID do autor.
    author_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Noticia {self.titulo}>'