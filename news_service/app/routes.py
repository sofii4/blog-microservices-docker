import os
import requests
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, 
    flash, g, current_app
)
from werkzeug.utils import secure_filename
from .models import Noticia
from . import db

# Configurações de validação
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
SUPERUSER_ID = 1

USERS_SERVICE_URL = os.environ.get("USERS_SERVICE_URL", "http://users-service")

bp = Blueprint('noticias', __name__)


@bp.before_request
def load_logged_in_user():
    """
    Load user_id and username from Redis session into g object.
    Makes them available to all templates.
    """
    g.user_id = session.get('user_id')
    g.username = session.get('username')

# Login verification decorator
def login_required(f):
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if g.user_id is None: 
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect('/cadastro/login')
        return f(*args, **kwargs)
    return decorated_function

# Helper functions
def get_author_username(author_id):
    """
    Fetch author username from users-service via internal API.
    Returns 'Unnamed Author' if unavailable.
    """
    try:
        url = f"{USERS_SERVICE_URL}/api/user/{author_id}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.json().get('username', 'Unnamed Author')
    except requests.exceptions.RequestException as e:
        current_app.logger.warning(f"Failed to reach users-service: {e}")
    return "Unnamed Author"

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(form_picture):
    """
    Save uploaded image to disk with validation.
    Returns filename or None if validation fails.
    """
    # Validate file size
    form_picture.seek(0, os.SEEK_END)
    file_size = form_picture.tell()
    form_picture.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f'Arquivo muito grande. Máximo {MAX_FILE_SIZE // (1024*1024)}MB.')
    
    # Validate file type
    if not allowed_file(form_picture.filename):
        raise ValueError(f'Tipo de arquivo não permitido. Extensões aceitas: {", ".join(ALLOWED_EXTENSIONS)}')
    
    filename = secure_filename(form_picture.filename)
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    form_picture.save(picture_path)
    return filename

# Main routes
@bp.route('/') 
def index():
    """Display all news articles with author information."""
    noticias_db = Noticia.query.order_by(Noticia.data_publicacao.desc()).all() 
    noticias_para_template = []
    for noticia in noticias_db: 
        author_name = get_author_username(noticia.author_id)
        noticias_para_template.append({
            'noticia': noticia,
            'author_name': author_name
        })
    return render_template('index.html', noticias_com_autor=noticias_para_template)

# Create news article
@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def criar_noticia():
    """Create a new news article with optional image upload."""
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        conteudo = request.form.get('conteudo', '').strip()
        
        # Validate required fields
        if not titulo:
            flash('Título é obrigatório.', 'danger')
            return redirect(url_for('noticias.criar_noticia'))
        
        if not conteudo:
            flash('Conteúdo é obrigatório.', 'danger')
            return redirect(url_for('noticias.criar_noticia'))
        
        filename = None
        imagem_file = request.files.get('imagem')
        
        if imagem_file and imagem_file.filename:
            try:
                filename = save_picture(imagem_file)
            except ValueError as e:
                flash(f'Erro no upload: {str(e)}', 'danger')
                return redirect(url_for('noticias.criar_noticia'))
        
        nova_noticia = Noticia(
            titulo=titulo,
            conteudo=conteudo,
            imagem=filename,
            author_id=g.user_id
        )
        db.session.add(nova_noticia)
        db.session.commit()
        
        flash('Notícia cadastrada com sucesso!', 'success')
        return redirect(url_for('noticias.index'))

    return render_template('criar_noticia.html')

# Delete news article
@bp.route('/noticias/delete/<int:noticia_id>', methods=('POST',))
@login_required
def delete_noticia(noticia_id):
    """
    Delete a news article.
    Only accessible to the article author or superuser.
    """
    noticia = Noticia.query.get_or_404(noticia_id)

    # Permission check: only author or superuser
    if g.user_id != SUPERUSER_ID and g.user_id != noticia.author_id:
        current_app.logger.warning(f"Unauthorized delete attempt by user {g.user_id} on article {noticia_id}")
        flash('Você não tem permissão para deletar este post.', 'danger')
        return redirect(url_for('noticias.index'))
    
    # Handle image deletion
    if noticia.imagem:
        filename_to_delete = noticia.imagem
        
        # Count other articles using the same image
        outros_posts_com_a_imagem = Noticia.query.filter(
            Noticia.imagem == filename_to_delete,
            Noticia.id != noticia_id
        ).count()
        
        # Only delete file if no other articles are using it
        if outros_posts_com_a_imagem == 0:
            try:
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename_to_delete)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    current_app.logger.info(f"Image deleted: {filename_to_delete}")
            except Exception as e:
                current_app.logger.error(f"Failed to delete image {filename_to_delete}: {e}")
        else:
            current_app.logger.info(f"Image {filename_to_delete} still in use by {outros_posts_com_a_imagem} articles")

    db.session.delete(noticia)
    db.session.commit()
    
    flash('Notícia deletada com sucesso.', 'success')
    return redirect(url_for('noticias.index'))


# Edit news article
@bp.route('/noticias/edit/<int:noticia_id>', methods=('GET', 'POST'))
@login_required
def edit_noticia(noticia_id):
    """
    Edit a news article.
    Only accessible to the article author or superuser.
    """
    noticia = Noticia.query.get_or_404(noticia_id)

    # Permission check: only author or superuser
    if g.user_id != SUPERUSER_ID and g.user_id != noticia.author_id:
        current_app.logger.warning(f"Unauthorized edit attempt by user {g.user_id} on article {noticia_id}")
        flash('Você não tem permissão para editar este post.', 'danger')
        return redirect(url_for('noticias.index'))

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        conteudo = request.form.get('conteudo', '').strip()
        
        # Validate required fields
        if not titulo:
            flash('Título é obrigatório.', 'danger')
            return redirect(url_for('noticias.edit_noticia', noticia_id=noticia_id))
        
        if not conteudo:
            flash('Conteúdo é obrigatório.', 'danger')
            return redirect(url_for('noticias.edit_noticia', noticia_id=noticia_id))
        
        noticia.titulo = titulo
        noticia.conteudo = conteudo
        
        # Handle image upload if provided
        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename:
            try:
                # Delete old image if exists
                if noticia.imagem:
                    try:
                        old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], noticia.imagem)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                            current_app.logger.info(f"Old image deleted: {noticia.imagem}")
                    except Exception as e:
                        current_app.logger.error(f"Failed to delete old image: {e}")

                # Save new image
                filename = save_picture(imagem_file)
                noticia.imagem = filename
            except ValueError as e:
                flash(f'Erro no upload: {str(e)}', 'danger')
                return redirect(url_for('noticias.edit_noticia', noticia_id=noticia_id))
        
        db.session.commit()
        flash('Notícia atualizada com sucesso!', 'success')
        return redirect(url_for('noticias.index'))

    return render_template('edit_noticia.html', noticia=noticia)