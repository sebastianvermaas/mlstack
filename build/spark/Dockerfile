FROM openjdk:8-jdk-slim-stretch

# Install package dependencies
RUN apt-get update && \
    apt-get install -y \
	  sudo \
	  curl \
	  vi \
	  nano \
	  python3 \
	  python3-pip && \
	apt-get clean && \
	apt-get autoremove

# Install Python dependencies
RUN pip3 install \
	  boto3 \
	  numpy \
	  pandas

# Install Spark
ARG spark_version=2.4.4
ARG hadoop_version=2.7

ENV SPARK_VERSION=${spark_version}
ENV HADOOP_VERSION=${hadoop_version}

COPY bin /tmp/
RUN chmod u+x /tmp/install-spark.sh && ./tmp/install-spark.sh
