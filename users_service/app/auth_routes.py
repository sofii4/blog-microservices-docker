
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
#importa do flask as ferramentas: registrar arquivo de rotas, renderizar os HTMLs, redirecionar o usuário, ler os dados fornecidos pelo usuário no form, mostrar as mensagens de sucesso/erro, conectar com redis.
from .models import User 
from . import db, bcrypt #importa conexão com bd

bp = Blueprint('auth', __name__) #registra o arquivo no flask
#permite a criação de links seguros "url_for('auth.login')"

# Cadastro de Usuários
@bp.route('/register', methods=('GET', 'POST')) #get mostra o form vazio, post salva os dados

def register(): 
    """Exibe e processa o formulário de registro."""
    if request.method == 'POST': #salvar: --> pega os dados crus do HTML:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verifica se o usuário ou email já existem
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first() 
        
        error = None 
        if user_exists: 
            error = 'Este nome de usuário já está em uso.' #atribui a mensagem de erro pra variável de erro
        elif email_exists: 
            error = 'Este e-mail já está em uso.' #atribui mensagem de erro pra variável de erro

        if error is None: 
            # Cria o novo usuário
            new_user = User(username=username, email=email) #gera o uername e email novo
            new_user.set_password(password) # chama o bcrypt que gera o hash (senha embaralhada)
            
            db.session.add(new_user)  
            db.session.commit() 
            
            flash('Registro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('auth.login'))
        
        flash(error, 'danger') # Se deu erro, exibe o erro

    return render_template('register.html') # Se for GET, apenas exibe a página


# login de usuário
@bp.route('/login', methods=('GET', 'POST')) 
def login():
    """Exibe e processa o formulário de login."""
    if request.method == 'POST': #se for POST, tenta encontrar o usuário no bd:
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first() 

        if user and user.check_password(password): # pega a senha digitada no login, gera um hash e compara com o hash registrado no banco (retorna V/F)

            # O Flask-Session salva isso no Redis
            session['user_id'] = user.id #pega o ID, registra no Redis e associa a um cookie de sessão que é enviado ao navegador
            session['username'] = user.username
            
            flash('Login realizado com sucesso!', 'success')
            
            # Redireciona para a página inicial do OUTRO serviço
            # A porta 80 (Traefik) vai rotear /noticias/ para o news-service
            return redirect('/noticias/')
        
        #se a verificação de username e senha não baterem:
        flash('Usuário ou senha inválidos.', 'danger')
    
    # Se for GET, apenas exibe a página
    return render_template('login.html')

# logout
@bp.route('/logout')
def logout():
    """Limpa a sessão (faz logout)."""
    
    session.clear() # O Flask-Session limpa os dados do Redis
    
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))