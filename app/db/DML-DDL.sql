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
INSERT INTO connectors_types (label,thumbnail_url,type_id) VALUES ('JSON','https://cdn.worldvectorlogo.com/logos/json.svg',2);
INSERT INTO connectors_types (label,thumbnail_url,type_id) VALUES ('CSV','https://static-00.iconduck.com/assets.00/csv-icon-448x512-rkoi7crs.png',3);
INSERT INTO connectors_types (label,thumbnail_url,type_id) VALUES ('EXCEL','https://cdn.worldvectorlogo.com/logos/excel-4.svg',4);
COMMIT;