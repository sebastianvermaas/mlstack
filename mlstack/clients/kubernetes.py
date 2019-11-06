
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

