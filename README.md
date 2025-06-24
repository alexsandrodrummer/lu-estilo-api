# 🛍️ Lu Estilo API

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org)

API moderna para gestão de produtos e vendas da Lu Estilo, desenvolvida com:

- **FastAPI** para endpoints rápidos e documentação automática
- **SQLAlchemy** + **Alembic** para ORM e migrações
- **PostgreSQL** como banco de dados principal
- **Docker** para containerização

## 🚀 Funcionalidades Principais

✔️ CRUD completo de produtos  
✔️ Autenticação via JWT  
✔️ Integração com gateways de pagamento  
✔️ Relatórios de vendas  
✔️ Documentação interativa (/docs e /redoc)  

## ⚙️ Configuração Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/alexsandrodrummer/lu-estilo-api.git

# 2. Suba os containers
docker-compose up -d --build

# 3. Acesse a API
http://localhost:8000/docs
