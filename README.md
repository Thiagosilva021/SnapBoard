# SnapBoard

O **SnapBoard** é uma aplicação web inspirada em plataformas de compartilhamento e descoberta de imagens, como o Pinterest.

O projeto está sendo desenvolvido com **Python e Flask**, com o objetivo de praticar conceitos de desenvolvimento web, autenticação de usuários, gerenciamento de banco de dados e construção de aplicações backend.

> **Status do projeto:** Em desenvolvimento

---

## Sobre o projeto

A ideia do SnapBoard é criar uma plataforma onde usuários possam criar suas contas e, futuramente, compartilhar, visualizar e organizar imagens em diferentes categorias e coleções.

O projeto foi criado como uma forma de colocar em prática conhecimentos de desenvolvimento **backend com Python**, além de integrar frontend, banco de dados e autenticação de usuários.

A proposta é evoluir gradualmente a aplicação até chegar a uma experiência semelhante a plataformas como o Pinterest.

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
│   │   │   └── theme.js
│   │   │
│   │   └── posts/
│   │
│   ├── templates/
│   │   ├── criar_conta.html
│   │   ├── feed.html
│   │   ├── homepage.html
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
├── .gitignore
├── criar_banco.py
├── main.py
├── README.md
└── requirements.txt
