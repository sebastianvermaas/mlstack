""" Module """

from mlstack.utils import logger, download_spark
from mlstack.clients import DockerClient, KubernetesClient


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

        repositories = [
            "tensorflow/tensorflow:latest-py3-jupyter",
            "openjdk:8-jdk-slim-stretch",
            "localstack/localstack:0.8.6",
        ]

        images = ["tensorflow", "spark"]
        dockerclient.pull_images(repositories=repositories)
        download_spark()
        dockerclient.build_images(images=images)

    def create(self):
        """ Creates an MLStack local Kubernetes cluster """
        logger.info("Creating an MLStack cluster in Kubernetes")
        KubernetesClient().create_manifests(
            ["spark", "tensorflow", "localstack"]
        )

    def close(self):
        """ Close the MLStack cluster """
        logger.info("Closing the MLStack cluster in Kubernetes")
        KubernetesClient().delete_manifests(
            ["spark", "tensorflow", "localstack"]
        )
