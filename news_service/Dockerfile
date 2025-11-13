
FROM python:3.10-slim-bookworm

# Variáveis de Ambiente:
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependências do Sistema:
# 'mysqlclient' (Python) precisa de bibliotecas do MariaDB/MySQL (Sistema)
# 'build-essential' é para compilar pacotes se necessário.
RUN apt-get update \
    && apt-get install -y build-essential default-libmysqlclient-dev pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./run.py .

# Cria um usuário "appuser" e dá a ele permissão do /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser

# Comando para iniciar o servidor.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "run:app"]
