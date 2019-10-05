FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04
RUN apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -yy && \
    apt-get update && \
    apt-get upgrade -yy && \
    apt-get install -yy git vim

ARG VERSION=2.0
ENV VERSION=$VERSION

RUN pip install tensorflow==$VERSION

RUN mkdir /opt/tensorflow
RUN mkdir /opt/tensorflow/input
COPY model.py /opt/tensorflow/input/model.py

RUN mkdir /opt/tensorflow/input/models/
RUN mkdir /opt/tensorflow/input/data
RUN mkdir /opt/tensorflow/input/scripts

WORKDIR /opt/tensorflow/input
ENTRYPOINT ["python", "model.py"]