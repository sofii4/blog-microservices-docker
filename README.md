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

---

Este é um projeto full-stack que implementa uma arquitetura de microserviços completa, containerizada com Docker. A aplicação é dividida em dois serviços independentes: um `users-service` (para registro, login, autenticação e gerenciamento de identidade) e um `news-service` (para o CRUD de notícias).

O sistema demonstra conceitos-chave de microserviços, incluindo um roteamento de requisições centralizado com um proxy reverso (Traefik), persistência de sessão compartilhada entre serviços usando Redis, e comunicação de serviço-para-serviço através de uma API REST interna (para buscar dados de autores).

## 🚀 Automação (CI/CD) com GitHub Actions

O projeto está configurado com um pipeline de **Integração Contínua (CI)** e **Entrega Contínua (CD)** usando o GitHub Actions, localizado em `.github/workflows/build-and-push.yml`.

Esse workflow é disparado automaticamente a cada `push` para a branch `main` e executa duas tarefas principais:

1.  **CI (Teste de Build):** O workflow constrói as imagens Docker para o `news-service` e o `users-service`. Se qualquer um dos builds falhar o workflow falha, protegendo o repositório.
2.  **CD (Entrega/Publicação):** Se os builds forem bem-sucedidos, o workflow faz login no Docker Hub e publica as novas imagens prontas para produção:
    * `sofii4/blog-news-service:latest`
    * `sofii4/blog-users-service:latest`
  
### 🛡️ Segurança e Manutenção Automática
Para manter os microsserviços protegidos contra vulnerabilidades:

* **Dependabot Alerts:** Monitoramento 24/7 de vulnerabilidades em bibliotecas Python e imagens base Docker.
* **Atualizações Semanais:** O Dependabot verifica semanalmente se existem versões mais recentes das dependências e abre Pull Requests automaticamente.

Isso garante que o Docker Hub sempre tenha a versão mais recente e funcional do código da branch `main`.

## 🛠️ Funcionalidades

### 🎨 Interface & UX
* **Design Moderno e Responsivo:** Interface construída com **TailwindCSS**, garantindo adaptação perfeita para mobile e desktop.
* **Dark Mode:** Suporte completo a tema escuro/claro com persistência de preferência do usuário via LocalStorage.
* **Interatividade:** Animações fluidas nos cards, modais para leitura de notícias e feedback visual em formulários.

### ⚙️ Backend & Arquitetura
* **Arquitetura de Microserviços:** Dois serviços Flask independentes (`users-service` e `news-service`).
* **Autenticação de Usuário:** Registro e login completos, com senhas hasheadas (Bcrypt).
* **Gerenciamento de Sessão:** Sessões compartilhadas entre os dois serviços usando **Redis**.
* **Proxy Reverso:** **Traefik** gerencia todo o tráfego de entrada, roteando para o serviço correto.
* **CRUD de Notícias:** Usuários podem criar, editar e deletar seus próprios posts.
* **Sistema de Permissão:**
    * **Usuário normal:** Só pode editar/deletar os posts que criou.
    * **Superusuário (ID 1):** Pode editar/deletar *qualquer* post.
* **API Interna:** O `news-service` consome uma API do `users-service` para buscar os nomes dos autores dos posts.
* **100% Containerizado:** Toda a arquitetura (Traefik, 2x Flask, 2x MariaDB, 1x Redis) é orquestrada com Docker Compose.

## ⚙️ Tecnologias Utilizadas

#### Front-end
* **TailwindCSS** (Estilização Utility-First)
* **HTML5 / Jinja2** (Templates)
* **JavaScript** (Lógica de Modais e Dark Mode)

#### Back-end (Framework & Servidor)
* **Python 3** / **Flask** / **Gunicorn**

#### Arquitetura & Orquestração
* **Docker** & **Docker Compose**
* **Traefik** (Proxy Reverso)

#### Banco de Dados & Sessões
* **MariaDB** (Duas instâncias separadas)
* **Redis** (Para o cache de sessão compartilhado)

## 📋 Requisitos do Sistema

- **Docker:** v20.10+
- **Docker Compose:** v1.29+
- **RAM:** Mínimo 2GB disponível
- **Espaço em disco:** ~3GB para todas as imagens
- **Portas disponíveis:** 8000, 8080


## 🔌Como Executar o Projeto

Esse projeto possui dois modos de execução: **Desenvolvimento** (modificar o código) e **Produção** (para rodar a aplicação em um servidor usando as imagens prontas).

### 1.  Modo de Desenvolvimento

Esse modo usa o `docker-compose.yml` padrão. Ele **constrói** as imagens localmente e usa "hot-reload" (reinicia o app quando você salva o código).

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/sofii4/blog-microservices-docker.git](https://github.com/sofii4/blog-microservices-docker.git)
    cd blog-microservices-docker
    ```

2.  **Crie o Arquivo de Ambiente (`.env`)**

    Crie um arquivo chamado `.env` na raiz do projeto. Este arquivo é **ignorado** pelo Git (`.gitignore`) e guarda seus segredos. Use o `.env.example` como modelo ou cole o conteúdo abaixo, substituindo as senhas:

    ```.env
    # Configuração do Flask (Mude DEBUG para 0 em produção)
    FLASK_APP=run.py
    FLASK_DEBUG=1
    SECRET_KEY=sua-chave-secreta-flask-super-forte-12345

    # Configuração do Redis
    SESSION_TYPE=redis
    SESSION_REDIS_URL=redis://redis-sessions:6379/0

    # --- Banco de Dados de Usuários ---
    USERS_DB_ROOT_PASSWORD=SuaSenhaROOTSuperForte123
    USERS_DB_DATABASE=users_db
    USERS_DB_USER=users_user
    USERS_DB_PASSWORD=SuaSenhaDeUsuarioForte456

    # --- Banco de Dados de Notícias ---
    NEWS_DB_ROOT_PASSWORD=OutraSenhaROOTSuperForte789
    NEWS_DB_DATABASE=noticias_db
    NEWS_DB_USER=noticias_user
    NEWS_DB_PASSWORD=OutraSenhaDeUsuarioForte101
    ```

3.  **Construa e Inicie os Containers**

    No seu terminal, na raiz do projeto, execute:
    ```bash
    docker compose up --build
    ```

4.  **Acesse a Aplicação (Desenvolvimento)**
    * **Página de Registro:** `http://localhost:8000/cadastro/register`
    * **Página de Login:** `http://localhost:8000/cadastro/login`
    * **Página Inicial (Notícias):** `http://localhost:8000/noticias/`
    * **Dashboard do Traefik:** `http://localhost:8080/`

5.  **Parando a Aplicação**
    Pressione `Ctrl+C` no terminal, ou (de outro terminal) rode `docker compose down`.

### 2.  Modo de Produção

Este modo usa o `docker-compose.prod.yml`. Ele **baixa** as imagens prontas do Docker Hub (que o GitHub Actions criou).

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/sofii4/blog-microservices-docker.git](https://github.com/sofii4/blog-microservices-docker.git)
    cd blog-microservices-docker
    ```

2.  **Crie o Arquivo de Ambiente (`.env`)**

    Siga o **"Passo 1"** da seção anterior para criar o arquivo `.env` **completo**. O arquivo de produção precisa de *todas* as variáveis (incluindo `USERS_DB_NAME`, `USERS_DB_USERNAME`, etc.) para que os bancos de dados iniciem corretamente.

3.  **Inicie os Containers (Produção)**

    Suba os containers:
    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```
    *(O `-d` inicia em modo "detached", ou segundo plano).*


4.  **Acesse a Aplicação (Produção)**

    O modo de produção usa a porta 8000 padrão:
    * **Página Inicial (Notícias):** `http://localhost:8000/noticias/`
    * **Página de Cadastro:** `http://localhost:8000/cadastro/register`
    * **Dashboard do Traefik:** `http://localhost:8080/`

    (Nota: Se estiver usando uma VM em modo NAT com redirecionamento de portas (ex: 8000 -> 80), você deve acessar pela porta do hospedeiro, como: `http://localhost:8000/noticias/`)

5.  **Parando a Aplicação (Produção)**

    Para parar e remover os volumes:

    ```bash
    docker compose -f docker-compose.prod.yml down --volumes
    ```


## 📚 Estrutura do Projeto

```
.
├── news_service/          # News Service (Flask)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py      # News model
│   │   ├── routes.py      # CRUD routes
│   │   ├── config.py      # Configuration
│   │   ├── templates/     # Jinja2 templates
│   │   └── static/
│   │       └── uploads/   # News images
│   ├── Dockerfile
│   └── requirements.txt
│
├── users_service/         # Users Service (Flask)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py      # User model
│   │   ├── auth_routes.py # Login/Register
│   │   ├── api_routes.py  # API for user data
│   │   ├── config.py
│   │   └── templates/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml     # Development configuration
├── docker-compose.prod.yml # Production configuration
├── .env.example           # Environment variables template
└── README.md
```


## 🏗️ Arquitetura Interna

```
Client (Browser)
    ↓
Traefik (Reverse Proxy on port 80/8000)
    ├── /cadastro → users-service:8000
    ├── /api → users-service:8000
    └── /noticias → news-service:8000
         ↓
    news-service communicates with users-service via internal HTTP
         ↓
    Both share session via Redis
         ↓
    Each service has its own MariaDB database
```

---

<div align="center">
  </br>
  <a href="https://www.linkedin.com/in/sofii4/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge">
  </a>
</div>