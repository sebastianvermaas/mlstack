#!/usr/bin/env bash

case "${AIRFLOW_ROLE}" in
  webserver)
    echo 'Starting Airflow webserver'
    exec airflow "${AIRFLOW_ROLE}"
    ;;
  scheduler)
    echo 'Starting Airflow scheduler'
    exec airflow "${AIRFLOW_ROLE}"
    ;;
  *)
    abort "Unsupported role ${AIRFLOW_ROLE}"
    ;;
esac
