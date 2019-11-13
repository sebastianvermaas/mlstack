FROM tensorflow/tensorflow:latest-gpu-py3-jupyter

RUN apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -yy && \
    apt-get update && \
    apt-get upgrade -yy && \
    apt-get install -yy git vim

RUN mkdir /usr/tensorflow
RUN mkdir /usr/tensorflow/input
COPY model.py /usr/tensorflow/input/model.py

RUN mkdir /usr/tensorflow/input/models
RUN mkdir /usr/tensorflow/input/data
RUN mkdir /usr/tensorflow/input/scripts

WORKDIR /usr/tensorflow/input

RUN useradd -ms /bin/bash mlstack
USER mlstack
ENTRYPOINT sleep 100000