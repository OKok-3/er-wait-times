-- Create the application database and schema
CREATE DATABASE open_wait_times OWNER owt_owner;

-- Work inside the database 
\connect open_wait_times;

-- Create the application schema
CREATE SCHEMA owt AUTHORIZATION owt_owner;

-- Grant ownership to application roles
GRANT USAGE ON SCHEMA owt TO owt_rw, owt_ro;