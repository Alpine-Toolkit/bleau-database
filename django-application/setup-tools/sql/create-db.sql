--

DROP DATABASE bleaudb;
DROP ROLE bleaudb;

CREATE ROLE bleaudb LOGIN
  PASSWORD 'bleaudb'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

CREATE DATABASE bleaudb
  WITH OWNER = bleaudb
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'fr_FR.UTF-8'
       LC_CTYPE = 'fr_FR.UTF-8'
       CONNECTION LIMIT = -1
       TEMPLATE template0;
GRANT ALL ON DATABASE bleaudb TO bleaudb;
REVOKE ALL ON DATABASE bleaudb FROM public;

COMMENT ON DATABASE bleaudb
  IS 'Bleau Database';

-- as superuser
\connect bleaudb
CREATE EXTENSION postgis;

-- End
