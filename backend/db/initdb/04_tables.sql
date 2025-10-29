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
  scraper_module  text NOT NULL,
  scraper_class   text NOT NULL,
  url             text NOT NULL,
  address         text NOT NULL,
  city            text NOT NULL,
  province        owt.province_code  NOT NULL,
  timezone        text DEFAULT 'America/Toronto',
  version         smallint NOT NULL
);

-- Scraped waiting times
CREATE TABLE owt.er_wait_times (
  hospital_id             text NOT NULL REFERENCES owt.hospital_metadata(id),
  fetch_ts                timestamptz NOT NULL,  -- The timestamp of the fetch operation
  update_ts               timestamptz NOT NULL,  -- The timestamp of the published last updated time of the fetched wait time
  wait_duration           interval NOT NULL,
  patient_arrival_time    timestamptz NOT NULL,
  patient_departure_time  timestamptz NOT NULL,
  extra_info              jsonb,  -- To store additional data that is hospital specific
  PRIMARY KEY (fetch_ts, hospital_id)
);