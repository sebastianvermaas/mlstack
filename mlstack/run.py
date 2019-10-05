""" Defines the MLStack class for running a local Kubernetes cluster """
from os import path, getcwd
import io
import ast
import yaml

import boto3
import docker
import kubernetes
from kubernetes.client import Configuration as KubeConfig

# from kubernetes.client import ExtensionsV1beta1Api as KubeExtensions
from kubernetes.client.apis.core_v1_api import CoreV1Api as KubeApi

from mlstack.utils import logger


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

        logger.info("Initializing MLStack")
        # GPU attribute may be overwritten by config
        self.gpu = False
        logger.warning("GPU set to %s ", self.gpu)

        if config_yaml:
            self.set_attributes(config_yaml)

        self.k8s_api = self.init_k8s()
        self.docker_api = self.init_docker()

    def set_attributes(self, config_yaml: str):
        """ Sets attributes based on a YAML configuration file """
        message = "Setting attributes for MLStack object from {config_yaml}".format(
            config_yaml=config_yaml
        )
        logger.info(message)

        config_path = path.join(getcwd(), config_yaml)
        with open(config_path, "r") as stream:
            try:

                for key, value in yaml.safe_load(stream).items():
                    setattr(self, key, value)
                    message = "Set attribute MLStack.{attr} to '{value}'".format(
                        attr=key, value=value
                    )
                    logger.info(message)

            except yaml.YAMLError as yamlerror:
                message = "Could not read and/or set attributes from {file}".format(
                    file=config_path
                )
                logger.error(message)
                raise yamlerror

    @staticmethod
    def init_k8s(kube_config: str = None):
        """
        Initializes a Kubernetes CoreV1Api object.

        Parameters
          kube_config: Path to a Kubernetes config file.
                       See `kubectl config set` for more
                       information.

        Returns
          k8s_api: A KubeApi object

        """
        logger.info("Initializing Kubernetes API")
        kubernetes.config.load_kube_config(kube_config)
        config = KubeConfig()
        config.assert_hostname = False
        KubeConfig.set_default(config)
        return KubeApi()

    @staticmethod
    def init_docker():
        """ Initializes a Docker APIClient. See `docker.APIClient` for more info """
        logger.info("Initializing Docker API")
        return docker.APIClient()

    @staticmethod
    def init_botoclient(service: str, endpoint_url: str):
        """
        Initializes an AWS S3 BotoClient for S3 and DynamoDB.

        Parameters
          service: Which AWS service to initialize a \
                   client for (i.e. `s3` or `dynamodb`)

        Returns
          botoclient: A Boto3 Client object.

        """
        logger.info("Initializing AWS Boto3 Client")
        botoclient = boto3.client(
            service,
            endpoint_url=endpoint_url,
            aws_access_key_id="foo",
            aws_secret_access_key="bar",
        )
        return botoclient

    def dockerbuild(self, build_tags: list = None):
        """
        Builds Docker images via the docker python API.

        Parameters
          build_tags: A list of tags to build. Assumes
                      that the image's Dockerfile is
                      located at
                      `ml-stack/build/{tag}/Dockerfile`

        """
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

            message = "Building Docker image {tag} from {path}".format(
                tag=tag, path=dockerfile_path
            )
            logger.info(message)

            byte_stream = io.BytesIO(dockerfile.encode("utf-8"))

            for line in self.docker_api.build(fileobj=byte_stream, rm=True, tag=tag):
                stream = ast.literal_eval(line.decode("utf-8")).get("stream", None)
                aux = ast.literal_eval(line.decode("utf-8")).get("aux", None)
                error = ast.literal_eval(line.decode("utf-8")).get("error", None)

                if stream:
                    logger.info(stream)
                elif aux:
                    logger.info(aux)
                elif error:
                    logger.error(error)
                else:
                    logger.warning("Include the key into this method")

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
