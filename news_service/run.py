
from app import create_app

# Chamada para criar e configurar a instância do app
app = create_app()

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8000)