
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from .models import User 
from . import db, bcrypt

bp = Blueprint('auth', __name__)

# User registration
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Display and process user registration form."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check for existing username or email
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first() 
        
        error = None 
        if user_exists: 
            error = 'Este nome de usuário já está em uso.'
        elif email_exists: 
            error = 'Este e-mail já está em uso.'

        if error is None: 
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)  
            db.session.commit() 
            
            flash('Registro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('auth.login'))
        
        flash(error, 'danger')

    return render_template('register.html')


# User login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Display and process user login form."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        user = User.query.filter_by(username=username).first() 

        if user and user.check_password(password):
            # Store session in Redis via Flask-Session
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash('Login realizado com sucesso!', 'success')
            
            # Redirect to news service main page
            # Traefik routes /noticias/ to news-service
            return redirect('/noticias/')
        
        flash('Usuário ou senha inválidos.', 'danger')
    
    return render_template('login.html')

# User logout
@bp.route('/logout')
def logout():
    """Clear session and logout user."""
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))