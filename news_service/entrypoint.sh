#!/bin/sh

# 1. Garante que a pasta existe
mkdir -p /app/app/static/uploads
chown -R appuser:appuser /app/app/static/uploads

# 2. Aguarda o banco de dados responder de verdade
echo "Aguardando o banco de dados..."
until gosu appuser python -c "
import os, sys, pymysql
try:
    pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE']
    )
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; do
    echo "Banco indisponível, aguardando..."
    sleep 2
done
echo "Banco disponível!"

# 3. Inicia o Gunicorn
echo "Iniciando Gunicorn como appuser..."
exec gosu appuser "$@"
```

---

## Correção 3 — `SECRET_KEY` com valor padrão do `.env.example`

Vejo nas variáveis de ambiente:
```
SECRET_KEY = sua-chave-secreta-flask-super-forte-12345