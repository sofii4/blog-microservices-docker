#!/bin/sh

# 1. Garante que a pasta existe antes de ajustar as permissões
mkdir -p /app/app/static/uploads

# 2. Ajusta permissões do volume em tempo de execução
chown -R appuser:appuser /app/app/static/uploads

# 3. Aguardar o Banco de Dados
echo "Aguardando o banco de dados..."
sleep 5 

# 4. Executa o CMD do Dockerfile como appuser
echo "Iniciando Gunicorn como appuser..."
exec gosu appuser "$@"