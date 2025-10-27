-- Base roles
CREATE ROLE owt_owner NOLOGIN;
CREATE ROLE owt_rw NOLOGIN;
CREATE ROLE owt_ro NOLOGIN;

-- Application roles
CREATE ROLE owt_admin     WITH LOGIN  INHERIT  CONNECTION  LIMIT 10;
CREATE ROLE owt_airflow   WITH LOGIN           CONNECTION  LIMIT 10;
CREATE ROLE owt_superset  WITH LOGIN           CONNECTION  LIMIT 10;

-- Memberships
GRANT owt_owner TO owt_admin;
GRANT owt_rw    TO owt_airflow;
GRANT owt_ro    TO owt_superset;

-- Set default search_path for application roles
ALTER ROLE owt_admin SET search_path TO owt, public;
ALTER ROLE owt_airflow SET search_path TO owt, public;
ALTER ROLE owt_superset SET search_path TO owt, public;