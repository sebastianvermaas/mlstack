""" Module """

from mlstack.utils import logger
from mlstack.clients import DockerClient


class MLStack:
    def __init__(self):
        logger.info("Initializing MLStack .. wohoo !")

    def setup(self, images: list):
        dockerclient = DockerClient()
        dockerclient.pull_images(images=["tensorflow/tensorflow"])
        dockerclient.build_images(images=[])
