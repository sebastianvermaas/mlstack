""" Submodule for defining general utility functions """
import binascii
import hashlib
import logging

# Sets the ml-stack logger
FORMAT = """%(asctime)s - %(levelname)s mlstack.%(module)s.%(funcName)s - %(message)s
"""

FORMATTER = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S")
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMATTER)

logger = logging.getLogger("ml-stack")
logger.setLevel(logging.INFO)
logger.addHandler(HANDLER)
