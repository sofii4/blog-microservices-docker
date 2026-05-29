# Site de Notícias em Microserviços

<img alt="Build Status" src="https://github.com/sofii4/blog-microservices-docker/actions/workflows/build-and-push.yml/badge.svg">

### Stack Principal

![Microservices](https://img.shields.io/badge/Architecture-Microservices-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Traefik](https://img.shields.io/badge/Proxy-Traefik-0D2232?style=for-the-badge&logo=traefikproxy&logoColor=white)
![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

---

Este projeto full-stack implementa uma arquitetura de microserviços containerizada com Docker. A aplicação é dividida em dois serviços independentes: um `users-service` para registro, login, autenticação e gerenciamento de identidade, e um `news-service` para o CRUD de notícias.

A solução agora também inclui monitoramento e observabilidade com **Prometheus** e **Grafana**. Os dois serviços Flask expõem métricas automaticamente via `prometheus_flask_exporter`, o Prometheus faz o scrape dessas métricas, e o Grafana é provisionado com datasource e dashboard prontos para uso.

## Visão Geral da Arquitetura

- `Traefik` centraliza o roteamento de entrada.
- `users-service` atende login, cadastro e API interna de dados de usuário.
- `news-service` atende o CRUD de notícias e consulta o `users-service` para nome de autores.
- `Redis` compartilha a sessão entre os serviços Flask.
- Cada serviço possui seu próprio banco `MariaDB`.
- `Prometheus` coleta métricas dos serviços e do Traefik.
- `Grafana` exibe o dashboard de observabilidade provisionado automaticamente.

## Monitoramento e Observabilidade

O monitoramento foi adicionado com a seguinte estrutura:

- `news-service` e `users-service` registram métricas HTTP automaticamente em `/metrics`.
- `Prometheus` consulta os jobs `news-service`, `users-service`, `traefik` e o próprio `prometheus`.
- `Grafana` usa o datasource do Prometheus em `http://prometheus:9090`.
- O dashboard `Microservices` é carregado automaticamente a partir de `monitoring/grafana/dashboards/microservices_overview.json`.

As métricas acompanhadas no dashboard incluem:

- taxa de requisições por serviço;
- taxa de erros 4xx/5xx;
- latência p50/p95;
- volume de requisições por status code;
- consumo por endpoint em `news-service` e `users-service`;
- tráfego do Traefik por rota e status.

## Automação com GitHub Actions

O projeto possui um pipeline de **Integração Contínua (CI)** e **Entrega Contínua (CD)** em `.github/workflows/build-and-push.yml`.

Esse workflow é executado a cada `push` na branch `main` e faz duas etapas principais:

1. Constrói as imagens Docker do `news-service` e do `users-service`.
2. Publica as imagens no Docker Hub quando o build passa com sucesso:
   - `sofii4/blog-news-service:latest`
   - `sofii4/blog-users-service:latest`

### Segurança e manutenção automática

- Dependabot monitora vulnerabilidades em dependências Python e imagens base Docker.
- Atualizações semanais são abertas automaticamente quando há versões novas disponíveis.

## Funcionalidades

### Interface e UX

- Interface responsiva com `TailwindCSS`.
- Tema escuro/claro com persistência via `LocalStorage`.
- Modais, feedback visual e animações nos cards de notícias.

### Backend e arquitetura

- Dois serviços Flask independentes: `users-service` e `news-service`.
- Autenticação com senhas hasheadas usando `Bcrypt`.
- Sessões compartilhadas entre os serviços usando `Redis`.
- Proxy reverso com `Traefik`.
- CRUD de notícias com controle de permissão por usuário.
- API interna para buscar dados de autores no `users-service`.
- Monitoramento com `Prometheus` e dashboards no `Grafana`.
- Toda a arquitetura é orquestrada com Docker Compose.

## Tecnologias Utilizadas

### Front-end

- `TailwindCSS`
- `HTML5` / `Jinja2`
- `JavaScript`

### Back-end

- `Python 3`
- `Flask`
- `Gunicorn`

### Observabilidade

- `Prometheus`
- `Grafana`
- `prometheus-flask-exporter`

### Orquestração e infraestrutura

- `Docker`
- `Docker Compose`
- `Traefik`

### Banco de dados e sessão

- `MariaDB`
- `Redis`

## Requisitos do Sistema

- Docker v20.10+
- Docker Compose v1.29+
- Pelo menos 2 GB de RAM disponível
- Cerca de 3 GB livres em disco para imagens e volumes
- Portas disponíveis: `8000`, `8080`, `9090`, `3000`

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto usando `.env.example` como base. Além das credenciais dos bancos e da chave secreta do Flask, o arquivo agora inclui variáveis para o Grafana.

Principais variáveis:

- `FLASK_APP`
- `FLASK_DEBUG`
- `SECRET_KEY`
- `SESSION_TYPE`
- `SESSION_REDIS_URL`
- `USERS_DB_ROOT_PASSWORD`
- `USERS_DB_DATABASE`
- `USERS_DB_USER`
- `USERS_DB_PASSWORD`
- `NEWS_DB_ROOT_PASSWORD`
- `NEWS_DB_DATABASE`
- `NEWS_DB_USER`
- `NEWS_DB_PASSWORD`
- `USERS_SERVICE_URL`
- `GRAFANA_ADMIN_USER`
- `GRAFANA_ADMIN_PASSWORD`

## Como Executar o Projeto

O projeto possui dois modos de execução: **Desenvolvimento** e **Produção**.

### 1. Modo de Desenvolvimento

Esse modo usa `docker-compose.yml`. Ele constrói as imagens localmente, ativa hot-reload e sobe também Prometheus e Grafana.

1. Clone o repositório.

```bash
git clone https://github.com/sofii4/blog-microservices-docker.git
cd blog-microservices-docker
```

2. Crie o arquivo `.env` na raiz do projeto.

Use o conteúdo de `.env.example` como base. Se preferir definir manualmente, siga a estrutura abaixo:

```env
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=sua-chave-secreta-flask-super-forte-12345

SESSION_TYPE=redis
SESSION_REDIS_URL=redis://redis-sessions:6379/0

USERS_DB_ROOT_PASSWORD=SuaSenhaROOTSuperForte123
USERS_DB_DATABASE=users_db
USERS_DB_USER=users_user
USERS_DB_PASSWORD=SuaSenhaDeUsuarioForte456

NEWS_DB_ROOT_PASSWORD=OutraSenhaROOTSuperForte789
NEWS_DB_DATABASE=noticias_db
NEWS_DB_USER=noticias_user
NEWS_DB_PASSWORD=OutraSenhaDeUsuarioForte101

USERS_SERVICE_URL=http://users-service:8000

GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

3. Suba os containers.

```bash
docker compose up --build
```

4. Acesse os serviços.

- Aplicação principal: `http://localhost:8000/noticias/`
- Cadastro: `http://localhost:8000/cadastro/register`
- Login: `http://localhost:8000/cadastro/login`
- Dashboard do Traefik: `http://localhost:8080/`
- Prometheus: `http://localhost:9090/`
- Grafana: `http://localhost:3000/`

O Grafana usa `admin` / `admin` por padrão, a menos que você sobrescreva `GRAFANA_ADMIN_USER` e `GRAFANA_ADMIN_PASSWORD` no `.env`.

5. Pare a aplicação.

```bash
docker compose down
```

### 2. Modo de Produção

Esse modo usa `docker-compose.prod.yml` e baixa as imagens publicadas no Docker Hub.

1. Clone o repositório e crie o `.env` como no modo de desenvolvimento.

2. Inicie os containers.

```bash
docker compose -f docker-compose.prod.yml up -d
```

3. Acesse os serviços.

- Aplicação principal: `http://localhost:8000/noticias/`
- Cadastro: `http://localhost:8000/cadastro/register`
- Login: `http://localhost:8000/cadastro/login`
- Dashboard do Traefik: `http://localhost:8080/`
- Prometheus: `http://localhost:9090/`
- Grafana: `http://localhost:3000/`

O Grafana usa `admin` / `admin` por padrão, a menos que você sobrescreva `GRAFANA_ADMIN_USER` e `GRAFANA_ADMIN_PASSWORD` no `.env`.

4. Pare a aplicação e remova os volumes.

```bash
docker compose -f docker-compose.prod.yml down --volumes
```

## Estrutura do Projeto

```text
.
├── docker-compose.yml
├── docker-compose.prod.yml
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── microservices_overview.json
│       └── provisioning/
│           ├── dashboards/
│           │   └── dashboards.yml
│           └── datasources/
│               └── prometheus.yml
├── news_service/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── run.py
│   └── app/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── routes.py
│       ├── static/
│       │   └── uploads/
│       └── templates/
│           ├── base.html
│           ├── criar_noticia.html
│           ├── edit_noticia.html
│           └── index.html
├── users_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│   └── app/
│       ├── __init__.py
│       ├── api_routes.py
│       ├── auth_routes.py
│       ├── config.py
│       ├── models.py
│       ├── static/
│       └── templates/
│           ├── base.html
│           ├── login.html
│           └── register.html
├── .env.example
├── README.md
└── troubleshooting.md
```

## Arquitetura Interna

```text
Client (Browser)
    ↓
Traefik (Reverse Proxy on port 8000/8080)
    ├── /cadastro → users-service:8000
    ├── /api → users-service:8000
    └── /noticias → news-service:8000
         ↓
    news-service comunica com users-service via HTTP interno
         ↓
    Ambos compartilham sessão via Redis
         ↓
    Cada serviço possui seu próprio MariaDB
         ↓
    Prometheus coleta métricas em /metrics e Traefik expõe métricas adicionais
         ↓
    Grafana exibe o dashboard provisionado automaticamente
```

## Troubleshooting Rápido

- Se o banco não subir, confira os valores do `.env` e rode `docker compose ps`.
- Se o `news-service` não encontrar o `users-service`, verifique se ambos estão na mesma rede `proxy-net`.
- Se Grafana abrir sem dados, confirme se o Prometheus está acessível em `http://prometheus:9090` dentro da rede Docker.
- Se a porta `8000`, `8080`, `9090` ou `3000` já estiver em uso, libere a porta ou ajuste o mapeamento no compose.

---

<div align="center">
  </br>
  <a href="https://www.linkedin.com/in/sofii4/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge">
  </a>
</div>