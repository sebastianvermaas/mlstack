""" Submodule for training a Tensorflow model """
from os import path
from datetime import datetime

import numpy as np
import tensorflow as tf

class TensorflowModel:
    """ Class for training a tensorflow model """
    model_savedir = "/opt/tensorflow/input/models"

    def __init__(self, model_json: str):
        self.filename = model_json.split("/")[-1].replace(".json", "")
        self.model = tf.keras.Model(model_json)

    def train(self, input_features: np.ndarray, ground_truth: np.ndarray, parameters: dict):
        """ Trains a model on a Tensorflow Pod """
        batch_size = parameters.get("batchSize", 64)
        epochs = parameters.get("numParameters", 10)

        self.model.fit(x=input_features, y=ground_truth, epochs=epochs, batch_size=batch_size)
        self.model.save(path.join(self.model_savedir, self.filename, datetime.now()))

