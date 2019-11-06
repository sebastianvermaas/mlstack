""" Submodule for defining general utility functions """
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
