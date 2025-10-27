#!/usr/bin/env bash

# Check needed env vars and fail if any is not set or empty
: "${OWT_ADMIN_PW:?OWT_ADMIN_PW is not set or is empty}"
: "${OWT_AIRFLOW_PW:?OWT_AIRFLOW_PW is not set or is empty}"
: "${OWT_SUPERSET_PW:?OWT_SUPERSET_PW is not set or is empty}"

# Set passwords for application roles
psql -v ON_ERROR_STOP=1 -U ${POSTGRES_USER} -d ${POSTGRES_DB:-postgres} <<SQL
ALTER ROLE owt_admin PASSWORD '${OWT_ADMIN_PW}';
ALTER ROLE owt_airflow PASSWORD '${OWT_AIRFLOW_PW}';
ALTER ROLE owt_superset PASSWORD '${OWT_SUPERSET_PW}';
SQL