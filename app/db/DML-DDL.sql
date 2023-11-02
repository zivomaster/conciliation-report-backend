-- Autor: Juan Alejandro Carrillo Jaimes
-- Empresa: Sophos Solutions
-- Fecha de Creación: 29-10-2023

-- ADDING UUID EXTENSION
-- check if the extension is installed
SELECT * FROM pg_extension WHERE extname = 'uuid-ossp';

-- INSTALAR UUID-OSSP
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CREATE USERS TABLE
CREATE TABLE users (
    user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_authenticated BOOLEAN NOT NULL DEFAULT FALSE
    is_superuser BOOLEAN NULL DEFAULT FALSE
);
-- CREATE TYPES TABLE
CREATE TABLE types(
    type_id SERIAL PRIMARY KEY,
    name VARCHAR(10) NOT NULL
);
-- CREATE AUTHENTICATION_METHODS TABLE
CREATE TABLE authentication_methods(
    auth_meth_id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    label VARCHAR(50) NOT NULL
);
-- CREATE CONNECTORS TABLE
CREATE TABLE connectors_types (
    contype_id SERIAL PRIMARY KEY,
    label VARCHAR(50) UNIQUE NOT NULL,
    thumbnail_url VARCHAR(300) NULL,
    type_id INT NULL,
    auth_meth_id INT NULL
);

-- CREATE DATABASE_CONNECTIONS TABLE
CREATE TABLE database_connections (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    connection_name VARCHAR(100) UNIQUE NOT NULL,
    hostname VARCHAR(1000) NULL,
    port INT NULL,
    database_name VARCHAR(100) NULL,
    username VARCHAR(100) NULL,
    password TEXT NULL,
    is_file BOOLEAN NULL DEFAULT FALSE,
    file TEXT NULL,
    separator VARCHAR(10) NULL,
    contype_id INT NULL,
    user_id UUID NULL,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
);

-- CREATE DATA_RULES TABLE [Homologaciones]

CREATE TABLE datarules_definition(
    datarules_definition_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL
);

CREATE TABLE datarules(
    datarules_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(500) NOT NULL,
    datarules_definition_id UUID NOT NULL
);

-- CREATE REPORT TABLE

CREATE TABLE reconciliation (
    reconciliation_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    code VARCHAR(100) NOT NULL,
    observations TEXT NULL,
    name VARCHAR(100) NOT NULL,
    origin_database VARCHAR(100) NOT NULL,
    reconciliation VARCHAR(200) NULL,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_execution TIMESTAMPTZ NULL,
    last_execution_done BOOLEAN NULL
);

-- ADDING FOREIGN KEY
ALTER TABLE connectors_types
ADD CONSTRAINT fk_types_id
FOREIGN KEY (type_id)
REFERENCES types (type_id);

ALTER TABLE connectors_types
ADD CONSTRAINT fk_auth_meth_id
FOREIGN KEY (auth_meth_id)
REFERENCES authentication_methods (auth_meth_id);

ALTER TABLE database_connections
ADD CONSTRAINT fk_connector_type_id
FOREIGN KEY (contype_id)
REFERENCES connectors_types (contype_id);

ALTER TABLE database_connections
ADD CONSTRAINT fk_user_id
FOREIGN KEY (user_id)
REFERENCES users (user_id);

ALTER TABLE datarules_definition
ADD CONSTRAINT fk_datarules_definition_id
FOREIGN KEY (datarules_definition_id)
REFERENCES datarules_definition (datarules_definition_id) ON DELETE CASCADE;

-- FUNCTION LAST_UPDATED

CREATE OR REPLACE FUNCTION update_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- TRIGGER LAST_UPDATED
CREATE TRIGGER files_last_updated
BEFORE UPDATE ON database_connections
FOR EACH ROW
EXECUTE FUNCTION update_last_updated();

-- FUNCTION LAST_UPDATED

-- TRIGGER LAST_UPDATED
CREATE TRIGGER report_last_updated
BEFORE UPDATE ON reconciliation
FOR EACH ROW
EXECUTE FUNCTION update_last_updated();


-- DML SENTENCES
-- INSERTS -> [types]
INSERT INTO types (name) VALUES ('DATABASE');
INSERT INTO types (name) VALUES ('JSON');
INSERT INTO types (name) VALUES ('CSV');
INSERT INTO types (name) VALUES ('EXCEL');
COMMIT;
-- INSERTS -> [authentication_methods]
INSERT INTO authentication_methods (type,label) VALUES ('USER_AND_PASSWORD','User and password');
INSERT INTO authentication_methods (type,label) VALUES ('SERVICE_ACCOUNT','Service account');
COMMIT;
-- INSERTS -> [connectors_types]
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('PostgreSQL','https://cdn.worldvectorlogo.com/logos/postgresql.svg',1,1);
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('BigQuery','https://cdn.icon-icons.com/icons2/2699/PNG/512/google_bigquery_logo_icon_168150.png',1,2);
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('MySQL','https://cdn.worldvectorlogo.com/logos/mysql-6.svg',1,1);
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('MongoDB','https://cdn.worldvectorlogo.com/logos/mongodb-icon-1.svg',1,1);
INSERT INTO connectors_types (label,thumbnail_url,type_id) VALUES ('CSV','https://static-00.iconduck.com/assets.00/csv-icon-448x512-rkoi7crs.png',3);
INSERT INTO connectors_types (label,thumbnail_url,type_id) VALUES ('EXCEL','https://cdn.worldvectorlogo.com/logos/excel-4.svg',4);
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('Oracle','https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.svg',1,1);
INSERT INTO connectors_types (label,thumbnail_url,type_id,auth_meth_id) VALUES ('SQLServer','https://cdn.worldvectorlogo.com/logos/microsoft-sql-server-1.svg',1,1);
COMMIT;