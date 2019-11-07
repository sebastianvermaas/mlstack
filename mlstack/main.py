""" Module """

from mlstack.utils import logger
from mlstack.clients import DockerClient


class MLStack:
    def __init__(self):
        logger.info("Initializing MLStack")

    def setup(self, images: list):
        logger.info(
            """
\n
        _      _           _
  _ __ | |  __| |_ __ _ __| |__
 | '  \| | (_-<  _/ _  / _| / /
 |_|_|_|_| /__/\__\__,_\__|_\_\
\n\n
 Local Kubernetes cluster for machine learning engineering

"""
        )
        logger.info("Setting up MLStack. This will take a little while. Grab a coffee!")
        dockerclient = DockerClient()
        dockerclient.pull_images(
            images=["tensorflow/tensorflow", "localstack/localstack"]
        )
        dockerclient.build_images(images=[])
