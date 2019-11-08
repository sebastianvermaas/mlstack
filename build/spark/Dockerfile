FROM openjdk:8-jdk-slim-stretch

# Install package dependencies
RUN apt-get update && \
    apt-get install -y \
	  sudo \
	  curl \
	  vim \
	  nano \
	  python3 \
	  python3-pip && \
	apt-get clean && \
	apt-get autoremove

ENV INSTALL_ROOT=/opt
ENV SPARK_HOME=${INSTALL_ROOT}/spark
ENV SPARK_CONF_DIR=${SPARK_HOME}/conf
ENV SPARK_ROLE=master

COPY bin/* /tmp/
RUN sudo tar -xzf "/tmp/spark-3.0.0-preview-bin-hadoop3.2.tgz" -C "${INSTALL_ROOT}/" --no-same-owner
RUN sudo mv /${INSTALL_ROOT}/spark-3.0.0-preview-bin-hadoop3.2 /${INSTALL_ROOT}/spark

WORKDIR ${SPARK_HOME}
RUN cp /tmp/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]