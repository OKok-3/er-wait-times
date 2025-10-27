\connect open_wait_times

-- Make sure nothing is created on public accidentally
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Only allow specific users to access the database
REVOKE CONNECT, TEMP ON DATABASE open_wait_times FROM PUBLIC;

-- Database level role specific privileges
GRANT CREATE        ON DATABASE open_wait_times TO owt_admin;
GRANT CONNECT, TEMP ON DATABASE open_wait_times TO owt_admin, owt_airflow, owt_superset;

-- Schema level role specific privileges
GRANT CREATE  ON SCHEMA owt TO owt_admin;
GRANT USAGE   ON SCHEMA owt TO owt_rw, owt_ro;

-- Ensure that everything is owned by owt_owner
SET ROLE owt_owner;

-- Table level role specific privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA owt GRANT SELECT ON TABLES TO owt_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA owt GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO owt_admin, owt_rw;

-- Sequence level role specific privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA owt GRANT SELECT ON SEQUENCES TO owt_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA owt GRANT SELECT, USAGE, UPDATE ON SEQUENCES TO owt_admin, owt_rw;