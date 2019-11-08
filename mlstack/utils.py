""" Submodule for defining general utility functions """
from pathlib import Path
import yaml
import urllib
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


def download_spark():
    """ Installs Spark """

    spark_url = (
        "http://apache.mirror.anlx.net/spark/spark-3.0.0-preview/"
        "spark-3.0.0-preview-bin-hadoop3.2.tgz"
    )

    spark_path = Path(
        str(Path(__file__).absolute()).replace("mlstack/utils.py", "build/spark/bin"),
        spark_url.split("/")[-1],
    )

    if spark_path.exists():
        logger.info("Spark Install file already exists")

    else:
        logger.info("Downloading Spark to %s\nfrom %s", spark_path, spark_url)
        urllib.request.urlretrieve(spark_url, spark_path)
