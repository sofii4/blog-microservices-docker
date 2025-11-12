
from flask import Blueprint, jsonify #registra o arquivo no Flask , transforma um objeto Python em uma string JSON
from .models import User 

#cria a API
bp = Blueprint('api', __name__) #registra o blueprint no flask com o nome "API"


@bp.route('/user/<int:user_id>') # qualquer número inteiro que vier depois de /user/ será capturado e entregue à função get_user como uma variável chamada user_id

def get_user(user_id):
    """Retorna dados de um usuário (JSON) pelo ID."""
    
    #procura no bd o username correspondente ao user-id fornecido
    user = User.query.get(user_id) # .get() --  atalho para buscar por Primary Key
    #agora essa variável é um objeto com os atributos is, username e email.

    if user: 
        return jsonify({  #retorna a resposta JSON com:
            'id': user.id, 
            'username': user.username,
            'email': user.email
        })
    else:
        return jsonify({'error': 'User not found'}), 404 #retorna o erro em um JSON com erro 404