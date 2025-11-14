#!/bin/sh

# 1. Dá ao 'appuser' a propriedade da pasta de uploads.
#    Isso conserta o volume montado no 'run time'.
chown -R appuser:appuser /app/app/static/uploads

# 2.  Garante que o 'appuser' é dono de tudo.
chown -R appuser:appuser /app

# 3. Entrega o controle para o 'CMD' (o gunicorn),
#    mas roda ele como o 'appuser' (drop de privilégios).
exec gosu appuser "$@"