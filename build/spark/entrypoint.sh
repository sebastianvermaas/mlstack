#!/usr/bin/env bash
source ~/.bashrc

function finish() {
    echo "Shutting down spark container"
}
trap finish EXIT

case "${SPARK_ROLE}" in
  master)
    exec "${SPARK_HOME}/bin/spark-class" org.apache.spark.deploy.master.Master
    ;;
  slave)
    exec "${SPARK_HOME}/bin/spark-class" org.apache.spark.deploy.worker.Worker "${SPARK_MASTER_HOST:-spark-master}:${SPARK_MASTER_PORT:-7077}"
    ;;
  history)
    mkdir -p "${SPARK_HOME}/logs/spark-events"
    exec "${SPARK_HOME}/bin/spark-class" org.apache.spark.deploy.history.HistoryServer
    ;;
  edge)
    sleep infinity
    ;;
  *)
    abort "Unsupported role ${SPARK_ROLE}"
    ;;
esac
