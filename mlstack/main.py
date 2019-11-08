""" Module """

from mlstack.utils import logger, download_spark
from mlstack.clients import DockerClient


class MLStack:
    def __init__(self):
        logger.info("Initializing MLStack")

    def setup(self):
        """
        Sets up MLStack by pulling Docker images, downloading dependencies,
        and building Docker images
        """
        logger.info(
            """

       _      _           _
 _ __ | |  __| |_ __ _ __| |__
| '  \| | (_-<  _/ _  / _| / /
|_|_|_|_| /__/\__\__,_\__|_\_\


Local Kubernetes cluster for machine learning engineering

        """
        )
        logger.info("Setting up MLStack. This will take a little while. Grab a coffee!")
        dockerclient = DockerClient()

        images = [
            "tensorflow/tensorflow:latest-py3-jupyter",
            "openjdk:8-jdk-slim-stretch",
            "localstack/localstack:0.8.6",
        ]
        dockerclient.pull_images(images=images)
        download_spark()
        dockerclient.build_images(images=["spark"])
