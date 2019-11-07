""" Defines a DockerClient class for building and pulling images """
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

    def pull_images(self, repositories: list):
        """
        Pulls images from Docker repositories

        Args
          repositories: Docker repositories to pull from

        """
        ids = list()
        for repository in repositories:
            logger.info("Pulling from %s\n", repository)
            for i, line in enumerate(self.pull(repository, stream=True, decode=True)):
                # Ideally there is a better way to do this
                if line.get("id", None):
                    ids.append(line.get("id"))
                    ids = list(set(ids))
                for id_ in ids:
                    if ("." not in id_) & (line.get("progress", None)):
                        if i % 15 == 0:
                            message = "{id}: {status} {progress}".format(
                                id=id_,
                                status=line.get("status"),
                                progress=line.get("progress"),
                            )
                            logger.info(message)
