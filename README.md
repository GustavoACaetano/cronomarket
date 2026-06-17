# Cronomarket - Trabalho Desenvolvimento Web

## Entrega Final

GitHub do Projeto: [GitHub](https://github.com/GustavoACaetano/cronomarket) \
Documento de gestão: [Docs](https://docs.google.com/document/d/1cFx1rhBcCupCJQpii3_imT73ekMZvBvEs4RNLiNn3Pc/edit?usp=sharing) \
Documentação de desenvolvimento (análise + projeto): [Docs](https://docs.google.com/document/d/1Z_OyYd8bQBoOX_jjxe5woGAxEXZSwEzyrMOBV0B_z2Y/edit?usp=sharing) \
Apresentação em slides: [Presentation](https://docs.google.com/presentation/d/1mQpT6WfIS4ljsbPTBo_Nq9sObr1AEehtI_ybN9D2PAw/edit?usp=sharing)

## Integrantes

- Davi Henrique Comério
- Gabriel de Paula Brunetti
- Gian Lucca Decoté Paneto Neves
- Gustavo Alves Caetano
- Heitor Lima Peixoto
- João Pedro Zamborlini Barcellos

## Como rodar?

### Backend

Pré-requisitos:

- Python 3.12 instalado.
- Pipenv instalado.
- Docker instalado.

Clone o repositório:

```bash
git clone https://github.com/GustavoACaetano/cronomarket.git
```

Entre na pasta do backend:

```bash
cd cronomarket/backend
```

Crie um arquivo `.env` na pasta `backend` com as variáveis do banco:

```env
POSTGRES_DB=cronomarket
POSTGRES_USER=cronomarket
POSTGRES_PASSWORD=cronomarket
```

Suba o banco PostgreSQL com Docker:

```bash
docker compose up -d
```

Instale as dependências:

```bash
pipenv install
```

Inicie o ambiente virtual:

```bash
pipenv shell
```

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Por padrão, o backend ficará disponível em `http://127.0.0.1:8000/`.

### Frontend

Pré-requisitos:

- NodeJS instalado.

Clone o repositório:

```bash
git clone https://github.com/GustavoACaetano/cronomarket.git
```

Abra um cmd na pasta `cronomarket` e instale as dependências:

```bash
npm install
```

Para executar em modo de desenvolvimento:

```bash
npm run dev
```

Para executar como preview, primeiro faça o build:

```bash
npm run build
```

E, então, rode em modo preview:

```bash
npm run preview
```
