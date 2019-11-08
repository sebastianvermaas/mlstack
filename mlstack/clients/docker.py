""" Defines a DockerClient class for building and pulling images """

import sys
from pathlib import Path

import docker
from mlstack.utils import logger


class DockerClient(docker.APIClient):
    """ Wrapper class for building and pulling images """

    def __init__(self):
        """ Initializes a DockerClient for building and pulling images """
        super().__init__()

    def build_images(self, images: list):
        """
        Builds Docker images from a Dockerfile.

        Args
          images: Images stored in mlstack/build/{image}, where the path
                  is a Docker build context containing a Dockerfile

        """
        for image in images:
            # Returns mlstack/build/{image} (where mlstack is the install directory)
            package_dir = str(
                str(Path(__file__).absolute()).replace(Path(__file__).name, "")
            )
            context_path = package_dir.replace(
                "mlstack/clients", "build/{image}".format(image=image)
            )
            logger.info("Building %s from %s", image, context_path)

            for line in self.build(
                path=context_path +"/.",
                tag="mlstack-{image}:latest".format(image=image),
                decode=True,
            ):

                if line.get("stream", None):
                    logger.info(line.get("stream"))
                elif line.get("error", None):
                    logger.error(line.get("error"))
                else:
                    logger.warning(line)

            logger.info("Successfully built %s", image)

    def pull_images(self, images: list):
        """
        Pulls images from Docker repositories

        Args
          repositories: Docker repositories to pull from

        """
        for image in images:
            logger.info("Pulling from %s\n", image)
            for line in self.pull(image, stream=True, decode=True):
                if (bool(line.get("status", False))) & ("." not in line.get("id", "")):
                    sys.stdout.write(
                        "\r{id}: {status} {progress}".format(
                            id=line.get("id", ""),
                            status=line.get("status", ""),
                            progress=line.get("progress", ""),
                        )
                    )
            print("\n")
