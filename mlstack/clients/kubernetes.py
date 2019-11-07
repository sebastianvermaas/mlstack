from pathlib import Path
import glob
import yaml
import kubernetes
from kubernetes.stream import stream
from kubernetes.client import V1DeleteOptions, AppsV1Api
from kubernetes.client import Configuration as KubeConfig
from kubernetes.client.apis.core_v1_api import CoreV1Api as KubeApi
from kubernetes.client.rest import ApiException as KubeApiException

from mlstack.utils import logger, read_yaml


class KubernetesClient(KubeApi):
    """
    Wrapper class for creating and deleting PVs and PVCs,
    and applying manifests
    """

    manifests_dir = str(
        str(Path(__file__).absolute())
        .replace(Path(__file__).name, "")
        .replace("mlstack/clients", "manifests")
    )

    def __init__(self):
        """ Initializes a KubernetesClient """
        kubernetes.config.load_kube_config()
        config = KubeConfig()
        config.assert_hostname = False
        KubeConfig.set_default(config)
        super().__init__()

    def create_manifest(self, components: list):
        """
        Creates a manifest from a list of components
        located in mlstack/manifests. Uses a clever
        getattr() trick to avoid hardcoding everything.

        Will create kubernetes apps in the following order:

         - Persistent Volume Claim
         - Persistent Volume
         - Config Map
         - Deployment
         - Secret
         - Service

        Args
          components: A list of mlstack component manifests to create.

        """
        for component in components:
            for app in [
                "persistent_volume_claim",
                "persist_volume",
                "config_map",
                "deployment",
                "secret",
                "service",
            ]:
                for file in glob.glob(
                    str(Path(self.manifests_dir, component)) + "/*.yaml"
                ):
                    mask = file.split("/")[-1].startswith(app.replace("_", "-"))
                    if Path(file).exists() & mask:
                        logger.info("Reading manifest from %s", file)
                        body = read_yaml(file)
                        name = body.get("metadata").get("name")

                        method = "create_namespaced_{app}".format(app=app)

                        try:
                            if app in [
                                "persistent_volume_claim",
                                "config_map",
                                "service",
                                "secret",
                            ]:

                                getattr(self, method)(namespace="default", body=body)
                            if app in ["persistent_volume"]:
                                getattr(self, "create_persistent_volume")(body=body)
                            if app in ["deployment"]:
                                AppsV1Api().create_namespaced_deployment(
                                    namespace="default", body=body
                                )
                        except KubeApiException:
                            logger.error(
                                "\n\nCannot create %s `%s` as it already exists.\n"
                                "Use `mlstack close <component>` if you want to recreate "
                                "the deployment\n",
                                "".join([a.capitalize() for a in app.split("_")]),
                                component,
                            )

                        logger.info(
                            "%s `%s` created",
                            "".join([a.capitalize() for a in app.split("_")]),
                            name,
                        )

    def delete_manifest(self, components: list):
        """
        Deletes a manifest from a list of components
        located in mlstack/manifests. Uses a clever
        getattr() trick to avoid hardcoding everything.

        Will delete kubernetes apps in the following order:

         - Persistent Volume Claim
         - Persistent Volume
         - Config Map
         - Deployment
         - Secret
         - Service

        Args
          components: A list of mlstack component manifests to create.

        """
        for component in components:
            for app in [
                "persistent_volume_claim",
                "persist_volume",
                "config_map",
                "deployment",
                "secret",
                "service",
            ]:
                for file in glob.glob(
                    str(Path(self.manifests_dir, component)) + "/*.yaml"
                ):
                    mask = file.split("/")[-1].startswith(app.replace("_", "-"))
                    if Path(file).exists() & mask:
                        logger.info("Reading manifest from %s", file)
                        body = read_yaml(file)
                        name = body.get("metadata").get("name")

                        method = "delete_namespaced_{app}".format(app=app)
                        try:

                            if app in [
                                "persistent_volume_claim",
                                "config_map",
                                "service",
                                "secret",
                            ]:
                                getattr(self, method)(
                                    namespace="default",
                                    name=name,
                                    body=V1DeleteOptions(),
                                )
                            if app in ["persistent_volume"]:
                                getattr(self, "create_persistent_volume")(
                                    body=V1DeleteOptions()
                                )
                            if app in ["deployment"]:
                                AppsV1Api().delete_namespaced_deployment(
                                    namespace="default",
                                    name=name,
                                    body=V1DeleteOptions(),
                                )

                            logger.info(
                                "%s `%s` deleted",
                                "".join([a.capitalize() for a in app.split("_")]),
                                name,
                            )
                        except KubeApiException:
                            logger.error(
                                "\n\nCannot delete %s `%s` as it does not exists.\n"
                            )
