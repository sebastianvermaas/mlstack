FROM tensorflow/tensorflow:latest-py3-jupyter

RUN apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -yy && \
    apt-get update && \
    apt-get upgrade -yy && \
    apt-get install -yy git vim

RUN mkdir /usr/mlstack
RUN mkdir /usr/mlstack/input
COPY model.py /usr/mlstack/input/model.py

RUN mkdir /usr/mlstack/input/models
RUN mkdir /usr/mlstack/input/data
RUN mkdir /usr/mlstack/input/scripts

WORKDIR /usr/mlstack/input

RUN useradd -ms /bin/bash mlstack
USER mlstack
ENTRYPOINT sleep infinity