# SnapBoard

O **SnapBoard** é uma aplicação web de compartilhamento e descoberta de imagens, inspirada em plataformas como o Pinterest — com perfis, feed, curtidas e um sistema de seguir usuários, no estilo de uma rede social.

Desenvolvido com **Python e Flask**, o projeto foi construído como prática de desenvolvimento backend, autenticação, modelagem de banco de dados, segurança web e integração entre frontend e backend, evoluindo de forma incremental até uma experiência mobile-first completa.

> **Status do projeto:** Em desenvolvimento ativo — funcionalidades principais implementadas.

---

## Funcionalidades

**Contas e autenticação**
- Cadastro com validação de e-mail e nome de usuário únicos
- Login/logout com sessão via Flask-Login
- Senhas com hash bcrypt (nunca armazenadas em texto puro)
- Proteção CSRF em todos os formulários e ações que alteram dados

**Perfil**
- Edição de perfil: nome de usuário, bio e foto de perfil
- Troca de senha (exige confirmação da senha atual)
- E-mail visível apenas para o próprio usuário — nunca exposto no perfil público
- Contadores de postagens, seguidores e seguindo

**Postagens**
- Upload de imagens com validação real de conteúdo (não confia só na extensão do arquivo)
- Preview da imagem antes de enviar
- Exclusão de postagens (arquivo + registro no banco, restrita ao dono)
- Download de imagens

**Feed e descoberta**
- Feed paginado, ordenado por mais recentes
- Busca de usuários por nome (funciona mesmo para quem ainda não postou nada)
- Curtidas persistentes, sem recarregar a página
- Sistema de seguir / deixar de seguir, com listas de seguidores e seguindo

**Interface**
- Design mobile-first, com navegação inferior fixa (estilo apps de rede social)
- Tema claro/escuro
- Tratamento de erros com páginas amigáveis (404, 403, 500)

---

## Tecnologias

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-WTF
- **Banco de dados:** SQLite
- **Frontend:** HTML, CSS e JavaScript puros (sem frameworks)
- **Outros:** Pillow (validação de imagens)

---

## Estrutura do projeto

```text
PROJETOSNAPBOARD/
│
├── instance/
│   └── snapboard.db
│
├── snapboard/
│   │
│   ├── static/
│   │   │
│   │   ├── css/
│   │   │   ├── auth.css
│   │   │   ├── base.css          # tokens de cor, navbar e navegação inferior compartilhados
│   │   │   ├── feed.css
│   │   │   ├── home.css
│   │   │   └── perfil.css
│   │   │
│   │   ├── img/
│   │   │   └── snapboard-logo.jpeg
│   │   │
│   │   ├── js/
│   │   │   ├── feed.js
│   │   │   ├── home.js
│   │   │   ├── perfil.js
│   │   │   ├── search.js
│   │   │   └── theme.js
│   │   │
│   │   ├── avatars/               # fotos de perfil enviadas pelos usuários
│   │   └── posts/                 # imagens das postagens
│   │
│   ├── templates/
│   │   ├── _bottom_nav.html       # navegação inferior (mobile), incluída nas páginas logadas
│   │   ├── atividade.html
│   │   ├── criar_conta.html
│   │   ├── editar_perfil.html
│   │   ├── erro.html              # páginas de erro (404/403/500)
│   │   ├── feed.html
│   │   ├── homepage.html
│   │   ├── lista_usuarios.html    # seguidores / seguindo
│   │   ├── login.html
│   │   └── perfil.html
│   │
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   └── routes.py
│
├── venv/
│
├── .env
├── .env.example
├── .gitignore
├── criar_banco.py
├── main.py
├── README.md
└── requirements.txt
```

---

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/Thiagosilva021/SnapBoard.git
cd SnapBoard

# 2. Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com sua própria SECRET_KEY e SQLALCHEMY_DATABASE_URI

# 5. Crie o banco de dados
python criar_banco.py

# 6. Rode a aplicação
python main.py
```

A aplicação sobe em `http://127.0.0.1:5000`.

---

## Próximos passos

- Evoluir a busca com resultados dedicados por usuário (além do que já filtra no feed)
- Sistema de notificações reais (curtidas e novos seguidores)
- Testes automatizados
