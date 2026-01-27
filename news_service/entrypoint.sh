#!/bin/sh

# 1. Ajusta permissões do volume em tempo de execução
chown -R appuser:appuser /app/app/static/uploads

# 2. (Opcional) Aguardar o Banco de Dados
# Isso evita que o Flask tente conectar antes do MariaDB estar pronto
echo "Aguardando o banco de dados..."
sleep 5 

# 3. Executa o CMD do Dockerfile como appuser
echo "Iniciando Gunicorn como appuser..."
exec gosu appuser "$@"