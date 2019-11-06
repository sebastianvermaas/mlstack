import kubernetes
from kubernetes.stream import stream
from kubernetes.client import V1DeleteOptions
from kubernetes.client import Configuration as KubeConfig
from kubernetes.client.apis.core_v1_api import CoreV1Api as KubeApi
from kubernetes.client.rest import ApiException as KubeApiException

from mlstack.utils import logger, read_yaml


class KubernetesClient(KubeApi):
    """
    Wrapper class for creating and deleting PVs and PVCs,
    and applying manifests
    """

    def __init__(self):
        """ Initializes a KubernetesClient """
        kubernetes.config.load_kube_config(kube_config)
        config = KubeConfig()
        config.assert_hostname = False
        KubeConfig.set_default(config)
        super().__init__()

    def create_persistent_volumes(self, pv_config: dict):
        """
        Creates Kubernetes persistent volumes. Checks if the persistent
        volumes already exist. If they do, no persistent volumes are created.
        If they do not, the persistent volumes are created based on a template.

        Args
          pv_map: Dictionary containing a key for the name of the persistent volume,
          		  along with associated storage and hostPath tags.

        """
        # Find out if the persistent volumes already exist
        existing = [
            items.metadata.name
            for items in self.list_persistent_volume().__dict__.get("_items")
        ]

        pv_template = """
        {{
            "kind": "PersistentVolume",
            "apiVersion": "v1",
            "metadata": {{
                "name": "{name}"
            }},
            "spec": {{
                "storageClassName": "manual",
                "capacity": {{
                    "storage": "{storage}"
                }},
                "accessModes": [
                    "ReadWriteMany"
                ],
                "hostPath": {{
                    "path": "{host_path}"
                }}
            }}
        }}
        """
        persistent_volumes = pv_map.keys()
        for persistent_volume in persistent_volumes:
            # Specify kubernetes persistent volume body configuration
            storage = pv_map.get(persistent_volume).get("storage")
            host_path = pv_map.get(persistent_volume).get("hostPath")

            persistent_volume_body = json.loads(
                pv_template.format(
                    name=persistent_volume, host_path=host_path, storage=storage,
                )
            )
            if persistent_volume in existing:
                logger.warning(
                    "Persistent Volume `%s` already exists.", persistent_volume,
                )
            else:
                logger.info(
                    "Creating Persistent Volume `%s` with body\n\n%s\n",
                    persistent_volume,
                    pformat(persistent_volume_body),
                )
                self.create_persistent_volume(body=persistent_volume_body, pretty=True)

    def _delete_persistent_volumes(self, persistent_volumes: list):
        """
        Deletes Persistent Volumes.
        Raises
          KubeApiException: If the persistent volume could not be deleted.
        """
        logger.info("Deleting persistent volumes %s", persistent_volumes)
        body = V1DeleteOptions()
        for persistent_volume in persistent_volumes:
            try:
                self.delete_persistent_volume(name=persistent_volume, body=body)
                logger.info("Deleted persistent volume `%s`", persistent_volume)
            except KubeApiException as err:
                logger.error(
                    "Exception when calling CoreV1Api "
                    "delete_persistent_volume: %s\n",
                    err,
                )
