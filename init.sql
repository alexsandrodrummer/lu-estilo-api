-- Criação de usuário e banco já são feitas automaticamente pelo PostgreSQL Docker
-- Aqui garantimos as permissões necessárias

GRANT ALL PRIVILEGES ON DATABASE lu_estilo_db TO lu_user;

\c lu_estilo_db

-- Configuração segura do schema public
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO lu_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lu_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lu_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO lu_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO lu_user;