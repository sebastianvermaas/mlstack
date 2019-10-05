""" Defines the MLStack class for running a local Kubernetes cluster """
from os import path, getcwd
import io
import yaml
import boto3
import docker
import kubernetes
from kubernetes.client import Configuration as KubeConfig
from kubernetes.client.apis.core_v1_api  import CoreV1Api as KubeApi


class MLStack:
    """ Instantiates the MLStack class for running a Kubernetes cluster """
    tensorflow_version = 2.0
    spark_version = 2.4.3

    endpoint_url_s3 = "http://127.0.0.1:30572"

    def __init__(self, config_yaml: str = None):
        """ Initializes MLStack. Can be configures with a YAML configuration file """
        if config_yaml:
            self.init_attributes(config_yaml)

        self.k8s_api = self.init_k8s()
        self.s3_client = self.init_botoclient("s3", self.endpoint_url_s3)

    def init_attributes(self, config_yaml: str):
        """ Sets attributes based on a YAML configuration file """
        config_path = path.join(getcwd(), config_yaml)
        with open(config_path, "r") as stream:
            try:
                for key, value in yaml.safe_load(stream).items():
                    print(key, value)
                    setattr(self, key, value)
            except yaml.YAMLError as exc:
                logger.error()

    @staticmethod
    def init_k8s():
        """ Initializes the Kubernetes CoreApiV1 """
kubernetes.config.load_kube_config()
config = KubeConfig()
config.assert_hostname = False
KubeConfig().set_default(config)
        return KubeApi()

    @staticmethod
    def init_botoclient(service: str, endpoint_url: str):
        """
        Create a new aws client connected to ENDPOINT_URL
        :return: an aws client
        """
        client = boto3.client(
            service,
            endpoint_url=endpoint_url,
            aws_access_key_id="foo",
            aws_secret_access_key="bar",
        )
        return client

    # def dockerbuild(self):
