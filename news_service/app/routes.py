

import os # pra interagir com sistema de arquivos (deletar imagens)
import requests #permite as API calls
from functools import wraps # pro decorador de login
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, 
    flash, g, current_app
)
#organizar as rotas, renderizar o html, acessar dados de um form, redirecionar p outra página, conectar com redis, "bloco de notas" pra cada requisição, mostrar mensagens de erro ou sucesso, pegar configurações globais.

from werkzeug.utils import secure_filename  #limpar nome do arquivo enviado
from .models import Noticia #importar o molde da tabela "Noticia" do bd
from . import db #importar a conexão com bd

bp = Blueprint('noticias', __name__)  #registrar o arquivo no flask


@bp.before_request # Executa antes de cada view
def load_logged_in_user():
    """
    Verifica se o user_id está na sessão (Redis) e o carrega no 'g'.
    Isso torna g.user_id e g.username disponíveis para TODOS os templates.
    """
    g.user_id = session.get('user_id') #pergunta ao redis o user_id
    g.username = session.get('username') #armazena o resultado no "bloco de notas"

# Verifica o login
def login_required(f): #checa o bloco de notas
    @wraps(f) 
    def decorated_function(*args, **kwargs):
        if g.user_id is None: 
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect('/cadastro/login')
        return f(*args, **kwargs)
    return decorated_function

# Rotas de apoio
def get_author_username(author_id): # API CALL 
    try:
        url = f"http://users-service:8000/api/user/{author_id}" #monta uma URL interna do Docker
        response = requests.get(url, timeout=3) #liga para o users-service 
        if response.status_code == 200: #se a ligação funcionou:
            return response.json().get('username', 'Autor Desconhecido') #pega a resposta JSON 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao contatar users-service: {e}")
    return "Autor (Erro)"

def save_picture(form_picture): #upload de imagem
    filename = secure_filename(form_picture.filename) #limpa o nome do arquivo (segurança)
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) #descobre o caminho onde salvar a imagem
    form_picture.save(picture_path) #salva o arquivo no disco
    return filename #retorna o nome da imagem pra salvar no banco

# Rotas principais
@bp.route('/') 
def index(): #busca posts no bd desse serviço, e busca os nomes dos autoes no users-service via API
    noticias_db = Noticia.query.order_by(Noticia.data_publicacao.desc()).all() 
    noticias_para_template = [] #cria uma lista com todos os POSTS
    for noticia in noticias_db: 
        author_name = get_author_username(noticia.author_id) #busca o nome via API
        noticias_para_template.append({ #adiciona o resultado na lista
            'noticia': noticia,
            'author_name': author_name
        })
    return render_template('index.html', noticias_com_autor=noticias_para_template) #renderiza as notícias completas

# Cadastrar um POST (notícia) 
@bp.route('/criar', methods=('GET', 'POST'))  #GET mostra um formulário em branco, POST salva no banco.
@login_required #chama a função de verificação de login
def criar_noticia(): 
    if request.method == 'POST': #salva:
        titulo = request.form['titulo'] 
        conteudo = request.form['conteudo']
        imagem_file = request.files.get('imagem')
        author_id = g.user_id # Pega o ID do bloco de notas
        
        filename = None
        if imagem_file:
            filename = save_picture(imagem_file) #chama a função de salvar imagem
        
        nova_noticia = Noticia( #cria um novo molde de notícia
            titulo=titulo,
            conteudo=conteudo,
            imagem=filename,
            author_id=author_id
        )
        db.session.add(nova_noticia)
        db.session.commit()
        
        flash('Notícia cadastrada com sucesso!', 'success')
        return redirect(url_for('noticias.index'))

    return render_template('criar_noticia.html') #se não for post, é get: mostrar formulário vazio


@bp.route('/noticias/delete/<int:noticia_id>', methods=('POST',)) #deletar notícia
@login_required #chama a função de verificação de login
def delete_noticia(noticia_id):
    """
    Deleta uma notícia.
    Acessível se o usuário for o autor OU o superusuário (ID 1).
    """
    noticia = Noticia.query.get_or_404(noticia_id) #encontra o POST da notícia no banco, se não -- ERRO 404

    # lógica de autenticação de permissão
    if g.user_id != 1 and g.user_id != noticia.author_id: 
        flash('Você não tem permissão para deletar este post.', 'danger')
        return redirect(url_for('noticias.index')) #redireciona pra home
    
    if noticia.imagem:
        # Pega o nome do arquivo que queremos deletar
        filename_to_delete = noticia.imagem
        
        # "Conte quantos OUTROS posts usam esta MESMA imagem"
        outros_posts_com_a_imagem = Noticia.query.filter(
            Noticia.imagem == filename_to_delete,
            Noticia.id != noticia_id  # Exclui o post que já estamos deletando
        ).count()
        
        # Só deleta o arquivo se ninguém mais o estiver usando
        if outros_posts_com_a_imagem == 0:
            try:
                # O caminho é relativo à pasta UPLOAD_FOLDER dentro do container
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename_to_delete)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"Arquivo {filename_to_delete} deletado do disco.")
            except Exception as e:
                print(f"Erro ao tentar deletar o arquivo de imagem: {e}")
        else:
            print(f"Arquivo {filename_to_delete} mantido no disco (em uso por outros {outros_posts_com_a_imagem} posts).")

    db.session.delete(noticia)
    db.session.commit()
    
    flash('Notícia deletada com sucesso.', 'success')
    return redirect(url_for('noticias.index'))


# Editar notícia
@bp.route('/noticias/edit/<int:noticia_id>', methods=('GET', 'POST')) #GET mostra o formulário preenchido, POST salva
@login_required #chama a função de verificação de login
def edit_noticia(noticia_id):
    """
    Exibe (GET) e processa (POST) o formulário de edição de uma notícia.
    Acessível se o usuário for o autor OU o superusuário (ID 1).
    """
    
    noticia = Noticia.query.get_or_404(noticia_id) # Encontra o POST no banco, se não -- ERRO 404

    # Regra de permissão
    if g.user_id != 1 and g.user_id != noticia.author_id:
        flash('Você não tem permissão para editar este post.', 'danger')
        return redirect(url_for('noticias.index')) #redireciona pra home

    if request.method == 'POST': #salva:
        # Atualiza os dados da notícia com o que veio do formulário
        noticia.titulo = request.form['titulo']
        noticia.conteudo = request.form['conteudo']
        
        # Checa se uma nova imagem foi enviada
        imagem_file = request.files.get('imagem')
        if imagem_file:
            # Deleta a imagem antiga, se ela existir
            if noticia.imagem:
                try:
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], noticia.imagem)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                except Exception as e:
                    print(f"Erro ao deletar imagem antiga: {e}")

            # Salva a nova imagem
            filename = save_picture(imagem_file)
            noticia.imagem = filename
        
        db.session.commit() # Salva as mudanças no banco (não usa .add pra não criar um novo, só atualiza)
        
        flash('Notícia atualizada com sucesso!', 'success')
        return redirect(url_for('noticias.index'))

    # Se for GET< renderizar um template preenchido com o objeto noticia
    return render_template('edit_noticia.html', noticia=noticia)