FROM puckel/docker-airflow

ARG requirements
RUN pip install ${requirements}

COPY bin/* /tmp/
RUN cp /tmp/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]