from . import db
from datetime import datetime

class Noticia(db.Model):
    """
    News article database model.
    Represents a news post with title, content, optional image, and metadata.
    """
    __tablename__ = 'noticia'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200), nullable=True)  # Stores only the filename
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, nullable=False)  # Foreign reference to users-service

    def __repr__(self):
        return f'<Noticia {self.titulo}>'