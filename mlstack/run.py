""" Defines the MLStack class for running a local Kubernetes cluster """
from os import path, getcwd
import io
import ast
import yaml
import logging

import boto3
import docker
import kubernetes
from kubernetes.client import Configuration as KubeConfig
from kubernetes.client import ExtensionsV1beta1Api as KubeExtensions
from kubernetes.client.apis.core_v1_api import CoreV1Api as KubeApi
from kubernetes.client.
global logger

FORMAT = "%(asctime)s - %(levelname)s mlstack.%(module)s.%(funcName)s - %(message)s"
FORMATTER = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S")

log_handler = logging.StreamHandler()
log_handler.setFormatter(FORMATTER)
logger = logging.getLogger("ml-stack")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


class MLStack:
    """ Instantiates the MLStack class for running a Kubernetes cluster """

    tensorflow_version = "2.0"
    spark_version = "2.4.3"
    endpoint_url_s3 = "http://127.0.0.1:30572"

    build_tags = ["tensorflow"]

    working_dir = getcwd()[: getcwd().index("ml-stack")]
    scripts_path = path.join(working_dir, "ml-stack/scripts")
    models_path = path.join(working_dir, "ml-stack/scripts")
    data_path = path.join(working_dir, "ml-stack/data")

    def __init__(self, config_yaml: str = None):
        """ Initializes MLStack. Can be configures with a YAML configuration file """
        # GPU attribute may be overwritten by config
        self.gpu = False

        if config_yaml:
            self.set_attributes(config_yaml)

        logger.info("Initializing Kubernetes API")
        self.k8s_api = self.init_k8s()

        logging.info("Initializing Docker API")
        self.docker_api = docker.APIClient()

    def set_attributes(self, config_yaml: str):
        """ Sets attributes based on a YAML configuration file """
        logger.info(
            "Setting attributes for MLStack object from {config_yaml}".format(
                config_yaml=config_yaml
            )
        )
        config_path = path.join(getcwd(), config_yaml)
        with open(config_path, "r") as stream:
            try:

                for key, value in yaml.safe_load(stream).items():
                    setattr(self, key, value)
                    logger.info(
                        "Set attribute MLStack.{attr} to '{value}'".format(
                            attr=key, value=value
                        )
                    )

            except yaml.YAMLError as exception:
                logging.error(
                    "Could not read and/or set attributes from {file}".format(
                        file=config_path
                    )
                )
                raise (exception)

    @staticmethod
    def init_k8s():
        """ Initializes the Kubernetes CoreApiV1 """
        kubernetes.config.load_kube_config()
        config = KubeConfig()
        config.assert_hostname = False
        KubeConfig.set_default(config)
        return KubeApi()

    @staticmethod
    def init_botoclient(service: str, endpoint_url: str):
        """
        Create a new aws client connected to ENDPOINT_URL
        :return: an aws client
        """
        logger.info("Initializing AWS Boto3 Client")
        client = boto3.client(
            service,
            endpoint_url=endpoint_url,
            aws_access_key_id="foo",
            aws_secret_access_key="bar",
        )
        logger.info("AWS Boto3 Client Initialized")
        return client

    def dockerbuild(self, build_tags: list = None):
        """ Builds Docker images """
        if build_tags is None:
            build_tags = self.build_tags

        for tag in build_tags:
            if self.gpu:
                tag = "-".join([tag, "gpu"])

            dockerfile_path = path.join(
                self.working_dir, "ml-stack/build", tag, "Dockerfile"
            )
            with open(dockerfile_path, "r") as dpath:
                dockerfile = dpath.read()

            f = io.BytesIO(dockerfile.encode("utf-8"))
            logger.info(
                "Building Docker image {tag} from {path}".format(
                    tag=tag, path=dockerfile_path
                )
            )

            for line in self.docker_api.build(fileobj=f, rm=True, tag=tag):
                stream = ast.literal_eval(line.decode("utf-8")).get("stream", None)
                aux = ast.literal_eval(line.decode("utf-8")).get("aux", None)
                error = ast.literal_eval(line.decode("utf-8")).get("error", None)

                logger.info(stream.replace("\n", "")) if stream else None
                logger.error(error.replace("\n", "")) if error else None

    def deploy(
        self, scripts_path: str = None, models_path: str = None, data_path: str = None
    ):
        """ Deploys MLStack to a local Kubernetes Cluster """
        if scripts_path is None:
            scripts_path = self.scripts_path
        if models_path is None:
            models_path = self.models_path
        if data_path is None:
            data_path = self.data_path

        raise NotImplementedError()

