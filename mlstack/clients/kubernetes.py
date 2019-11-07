""" Defines a DockerClient class for creating and deleting manifests """
from pathlib import Path
import glob
import re

import kubernetes
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

    def create_manifests(self, components: list):
        """ Creates Kubernetes manifests """
        for component in components:
            self.create_manifest(component=component)

    def delete_manifests(self, components: list):
        """ Deletes Kubernetes manifests """

        for component in components:
            self.delete_manifest(component=component)

    def create_manifest(self, component: str):
        """
        Creates a manifest from a list of components
        located in mlstack/manifests. Uses a clever
        getattr() trick to avoid hardcoding everything.

        Will create kubernetes apps in the following order:

         - PersistentVolumeClaim
         - PersistentVolume
         - ConfigMap
         - Deployment
         - Secret
         - Service

        Args
          components: A list of mlstack component manifests to create.

        """
        for file in glob.glob(str(Path(self.manifests_dir, component)) + "/*.yaml"):
            body = read_yaml(file)
            kind = body.get("kind")
            name = body.get("metadata").get("name")
            method_ext = "_".join(
                val.lower() for val in re.findall("[A-Z][^A-Z]*", kind)
            )

            if kind in ["PersistentVolumeClaim", "ConfigMap", "Service", "Secret"]:
                try:
                    method = "create_namespaced_{ext}".format(ext=method_ext)
                    getattr(self, method)(namespace="default", body=body)
                    logger.info("%s `%s` created", kind, name)

                except KubeApiException:
                    logger.error(
                        "\n\nCannot create %s `%s` as it already exists.\n"
                        "Use `mlstack close `%s` if you want to recreate "
                        "the deployment\n",
                        kind,
                        name,
                        component,
                    )

            if kind in ["PersistentVolume"]:
                try:
                    getattr(self, "create_persistent_volume")(body=body)
                    logger.info("%s `%s` created", kind, name)

                except KubeApiException:
                    logger.error(
                        "\n\nCannot create %s `%s` as it already exists.\n"
                        "Use `mlstack close `%s` if you want to recreate "
                        "the deployment\n",
                        kind,
                        name,
                        component,
                    )
            if kind in ["Deployment"]:
                try:

                    AppsV1Api().create_namespaced_deployment(
                        namespace="default", body=body
                    )
                    logger.info("%s `%s` created", kind, name)

                except KubeApiException:
                    logger.error(
                        "\n\nCannot create %s `%s` as it already exists.\n"
                        "Use `mlstack close `%s` if you want to recreate "
                        "the deployment\n",
                        kind,
                        name,
                        component,
                    )

    def delete_manifest(self, component: str):
        """
        Deletes a manifest from a list of components
        located in mlstack/manifests. Uses a clever
        getattr() trick to avoid hardcoding everything.

        Will create kubernetes apps in the following order:

         - PersistentVolumeClaim
         - PersistentVolume
         - ConfigMap
         - Deployment
         - Secret
         - Service

        Args
          components: A list of mlstack component manifests to create.

        """
        for file in glob.glob(str(Path(self.manifests_dir, component)) + "/*.yaml"):
            body = read_yaml(file)
            kind = body.get("kind")
            name = body.get("metadata").get("name")
            method_ext = "_".join(
                val.lower() for val in re.findall("[A-Z][^A-Z]*", kind)
            )

            if kind in ["PersistentVolumeClaim", "ConfigMap", "Service", "Secret"]:
                try:
                    method = "delete_namespaced_{ext}".format(ext=method_ext)
                    getattr(self, method)(
                        namespace="default", name=name, body=V1DeleteOptions()
                    )
                    logger.info("%s `%s` deleted", kind, name)

                except KubeApiException:
                    logger.error(
                        "Cannot delete %s `%s` as it already exists.", kind, name
                    )

            if kind in ["PersistentVolume"]:
                try:
                    getattr(self, "delete_persistent_volume")(
                        name=name, body=V1DeleteOptions()
                    )
                    logger.info("%s `%s` deleted", kind, name)

                except KubeApiException:
                    logger.error(
                        "Cannot delete %s `%s` as it already exists.", kind, name
                    )

            if kind in ["Deployment"]:
                try:
                    AppsV1Api().delete_namespaced_deployment(
                        namespace="default", name=name, body=V1DeleteOptions()
                    )
                    logger.info("%s `%s` deleted", kind, name)

                except KubeApiException:
                    logger.error(
                        "Cannot delete %s `%s` as it already exists.", kind, name
                    )
