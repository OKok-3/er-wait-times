\connect open_wait_times
SET ROLE owt_owner;

-- Create shared types for the various tables
CREATE TYPE owt.province_code AS ENUM 
  ('AB','BC','MB','NB','NL','NS','NT','NU','ON','PE','QC','SK','YT');
GRANT USAGE ON TYPE owt.province_code TO owt_rw, owt_ro;

-- Hospital metadata
CREATE TABLE owt.hospital_metadata (
  id              text PRIMARY KEY,
  name            text NOT NULL,
  dept            varchar(20) NOT NULL,
  address         text NOT NULL,
  county          text NOT NULL,
  city            text NOT NULL,
  province        owt.province_code  NOT NULL,
  timezone        text NOT NULL CHECK (timezone ~ '^[A-Za-z]+\/[A-Za-z_+-]+$'),
  url             text NOT NULL CHECK (url ~ '^https?:\/\/'),
  scraper_module  text NOT NULL,
  scraper_class   text NOT NULL,
  version         smallint NOT NULL CHECK (version > 0)
);

-- Fetch logs
CREATE TABLE owt.fetch_logs (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  hospital_id       text NOT NULL REFERENCES owt.hospital_metadata(id) ON DELETE RESTRICT,
  ts                timestamptz NOT NULL,
  status_code       smallint NOT NULL CHECK (status_code >= 100 AND status_code < 600),
  error             text,
  file_hash         text,
  file_name         text,
  UNIQUE (hospital_id, ts),
  -- Only allow file hash and name to be null iff there is an error
  CONSTRAINT fetch_log_error_check CHECK (
    (error IS NULL      AND file_hash IS NOT NULL AND file_name IS NOT NULL) OR
    (error IS NOT NULL  AND file_hash IS NULL     AND file_name IS NULL)
  )
);

-- Scraped waiting times
CREATE TABLE owt.er_wait_times (
  fetch_log_id            uuid NOT NULL REFERENCES owt.fetch_logs(id),
  hospital_id             text NOT NULL REFERENCES owt.hospital_metadata(id) ON DELETE RESTRICT,
  update_ts               timestamptz NOT NULL,  -- The timestamp of the published last updated time of the fetched wait time
  wait_duration           interval NOT NULL,
  patient_arrival_time    timestamptz NOT NULL,
  patient_departure_time  timestamptz NOT NULL,
  extra_info              jsonb,  -- To store additional data that is hospital specific
  PRIMARY KEY (hospital_id, fetch_log_id),
  CONSTRAINT er_wait_times_patient_departure_time_check CHECK (patient_departure_time > patient_arrival_time),
  CONSTRAINT er_wait_times_wait_duration_check CHECK (wait_duration > INTERVAL '0 seconds')
);
