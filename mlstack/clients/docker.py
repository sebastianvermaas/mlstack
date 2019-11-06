""" Defines a DockerClient class for building and pulling images """
import tqdm
from pathlib import Path

import docker
from mlstack.utils import logger


class DockerClient(docker.APIClient):
    """ Wrapper class for building and pulling images """

    def __init__(self):
        """ Initializes a DockerClient for building and pulling images """
        super().__init__()

    def pull_images(self, repositories: list):
        """
        Pulls images from Docker repositories
        """
        ids = list()
        for repository in repositories:
            logger.info("Pulling from %s\n", repository)
            for i, line in enumerate(self.pull(repository, stream=True, decode=True)):
                if line.get("id", None):
                    ids.append(line.get("id"))
                    ids = list(set(ids))
                for id in ids:
                    if "." not in id:
                        if line.get("progressDetail", None):
                            if i % 15== 0:
                                logger.info("{id}: {status} {progress}".format(id=id, status=line.get("status"), progress=line.get("progress")))

    def build_images(self, images: list):
        """
        Builds Docker images from a Dockerfile.
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
                path=context_path,
                tag="mlstack-{image}:latest".format(image=image),
                decode=True,
            ):

                if line.get("stream", None):
                    logger.info(line.get("stream"))
                elif line.get("error", None):
                    logger.error(line.get("error"))
                else:
                    logger.warning(line)

            logger.info("Woohoo! Successfully built %s", image)
