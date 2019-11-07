""" Submodule for defining general utility functions """
import yaml
import binascii
import hashlib
import logging

# Sets the ml-stack logger
FORMAT = """%(asctime)s - %(levelname)s mlstack.%(module)s - %(message)s"""
FORMATTER = logging.Formatter(FORMAT, "%H:%M:%S")
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)
logger = logging.getLogger("mlstack")
logger.setLevel(logging.INFO)
logger.addHandler(HANDLER)


def read_yaml(config_path: str = None):
    """
    Reads a configuration YAML.
    If None is specified, returns an empty dictionary
    Args
      config_path: Absolute path to a Configuration file

    """
    if not config_path:
        return {}

    with open(config_path) as stream:
        try:
            return list(yaml.load_all(stream))

        except yaml.YAMLError as yamlerror:
            message = "Could not read and/or set "
            "attributes from {file}".format(file=config_path)
            logger.error(message)
            raise yamlerror


def install_dependencies():
    spark_version = "2.4.4"
    urls = [
        "http://apache.mirror.anlx.net/spark/spark-{spark_version}/spark-"
        "{spark_version}-bin-without-hadoop.tgz".format(spark_version=spark_version)
    ]
