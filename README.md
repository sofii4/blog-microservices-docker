# Blog de Notícias em Microserviços (Flask & Docker)

<img alt="Build Status" src="https://github.com/sofii4/blog-microservices-docker/actions/workflows/build-and-push.yml/badge.svg">

Este é um projeto de blog full-stack que implementa uma arquitetura de microserviços completa, containerizada com Docker. A aplicação é dividida em dois serviços independentes: um `users-service` (para registro, login, autenticação e gerenciamento de identidade) e um `news-service` (para o CRUD de notícias).

O sistema demonstra conceitos-chave de microserviços, incluindo um roteamento de requisições centralizado com um proxy reverso (Traefik), persistência de sessão compartilhada entre serviços usando Redis, e comunicação de serviço-para-serviço através de uma API REST interna (para buscar dados de autores).

##  Automação (CI/CD) com GitHub Actions

O projeto está configurado com um pipeline de **Integração Contínua (CI)** e **Entrega Contínua (CD)** usando o GitHub Actions, localizado em `.github/workflows/build-and-push.yml`.

Esse workflow é disparado automaticamente a cada `push` para a branch `main` e executa duas tarefas principais:

1.  **CI (Teste de Build):** O workflow constrói as imagens Docker para o `news-service` e o `users-service`. Se qualquer um dos builds falhar o workflow falha, protegendo o repositório.
2.  **CD (Entrega/Publicação):** Se os builds forem bem-sucedidos, o workflow faz login no Docker Hub e publica as novas imagens prontas para produção:
    * `sofii4/blog-news-service:latest`
    * `sofii4/blog-users-service:latest`

Isso garante que o Docker Hub sempre tenha a versão mais recente e funcional do código da branch `main`.

## Funcionalidades

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

## Tecnologias Utilizadas

#### Back-end (Framework & Servidor)
* **Python 3** / **Flask** / **Gunicorn**

#### Arquitetura & Orquestração
* **Docker** & **Docker Compose**
* **Traefik** (Proxy Reverso)

#### Banco de Dados & Sessões
* **MariaDB** (Duas instâncias separadas)
* **Redis** (Para o cache de sessão compartilhado)

---

##  Como Executar o Projeto

Esse projeto possui dois modos de execução: **Desenvolvimento** (modificar o código) e **Produção** (para rodar a aplicação em um servidor usando as imagens prontas).

### 1. Como Executar em Modo de Desenvolvimento

Esse modo usa o `docker-compose.yml` padrão. Ele **constrói** as imagens localmente e usa "hot-reload" (reinicia o app quando você salva o código).

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/sofii4/blog-microservicos-flask.git](https://github.com/sofii4/blog-microservicos-flask.git)
    cd blog-microservicos-flask
    ```

2.  **Crie o Arquivo de Ambiente (`.env`)**

    Crie um arquivo chamado `.env` na raiz do projeto. Este arquivo é **ignorado** pelo Git (`.gitignore`) e guarda seus segredos. Use o `.env.example` como modelo ou cole o conteúdo abaixo, substituindo as senhas:

    ```.env
    # Arquivo: .env 

    # Segredo do Flask
    FLASK_SECRET_KEY=sua-chave-secreta-flask-super-forte-12345

    # Segredos para news-service
    NEWS_DB_PASSWORD=Sophia866
    NEWS_ROOT_PASSWORD=Sophia866

    # Segredos para users-service
    USERS_DB_PASSWORD=OutraSenhaForte123
    USERS_ROOT_PASSWORD=OutraSenhaForte123
    ```

3.  **Construa e Inicie os Containers**

    No seu terminal, na raiz do projeto, execute:
    ```bash
    docker compose up --build
    ```
    (Pode demorar alguns minutos para construir as imagens).

4.  **Acesse a Aplicação (Desenvolvimento)**
    * **Página de Registro:** `http://localhost:8000/cadastro/register`
    * **Página de Login:** `http://localhost:8000/cadastro/login`
    * **Página Inicial (Notícias):** `http://localhost:8000/noticias/`
    * **Dashboard do Traefik:** `http://localhost:8080/`

5.  **Parando a Aplicação**
    Pressione `Ctrl+C` no terminal, ou (de outro terminal) rode `docker compose down`.

### 2. Como Executar em Modo de Produção

Esse modo usa o `docker-compose.prod.yml`. Ele **não** constrói nada; ele **baixa** as imagens prontas do Docker Hub (que o GitHub Actions criou).

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/sofii4/blog-microservicos-flask.git](https://github.com/sofii4/blog-microservicos-flask.git)
    cd blog-microservicos-flask
    ```

2.  **Crie o Arquivo de Ambiente (`.env`)**

    Siga o **mesmo Passo 2** do modo de desenvolvimento. O arquivo de produção lê os mesmos segredos.

3.  **Execute as Migrações do Banco**

    Como os bancos de dados estão vazios, precisamos criar as tabelas *antes* de ligar os apps. Usamos o comando `run` para isso:

    ```bash
    # (O -f aponta para o arquivo de produção)
    docker compose -f docker-compose.prod.yml run --rm users-service flask db upgrade
    docker compose -f docker-compose.prod.yml run --rm news-service flask db upgrade
    ```
    *(O `--rm` remove o container temporário após a execução).*

4.  **Inicie os Containers (Produção)**
    Agora, suba o stack completo em modo "detached" (`-d`):
    ```bash
    docker compose -f docker-compose.prod.yml up -d
    ```

5.  **Acesse a Aplicação (Produção)**
    O modo de produção usa a porta 80 padrão:
    * **Página de Registro:** `http://localhost/cadastro/register`
    * **Página de Login:** `http://localhost/cadastro/login`
    * **Página Inicial (Notícias):** `http://localhost/noticias/`
    * **Dashboard do Traefik:** `http://localhost:8080/`

6.  **Parando a Aplicação (Produção)**
    ```bash
    docker compose -f docker-compose.prod.yml down
    ```