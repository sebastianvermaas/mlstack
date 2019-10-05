# Machine Learning Stack
![release](https://img.shields.io/badge/release-v0.0.1-blue)
![Black Logo](https://img.shields.io/badge/code%20style-black-000000.svg)
> *Initial work! No promise on functionality or up to date documentation*

It is common for data scientists to be well equipped in languages and packages commonly used for statistical analysis and modelling. It is less common that data scientits are equipped to properly implement those models at a production level while adhering to software engineering principles.

**ml-stack** provides a local development stack for data scientists that imitate production environments.

## Setup

### Dependencies
Initial versions assume that you have **Ubuntu 18.04** as your operating system. Later versions may include other operating systems, GPU/non-gpu support, and dynamic OS checks.


```bash
git clone https://github.com/sebastianvermaas/ml-stack.git

cd ml-stack

# Installs dependencies (not implemented)
sudo ./install.sh

# Sets up conda virtual environment
conda env create -f conda.yml
conda activate ml

# Builds docker images
ml-stack build --tags "tensorflow-gpu"

# Deploys to local Kubernetes cluster (not implemented)
ml-stack deploy --containers "tensorflow-gpu"

```

## Design
The design is in terms of the Kubernetes Pods. TODO: include Miniconda development with Jupyter and NVIDIA GPU support.

<p align="center">
    <img src='docs/design.png' height=300>
</p>


### Components
- [**Conda**](#conda): A minimal Anaconda environment for local development
- [**Docker / Kubernetes**](#kubernetes): Base images and Pod executables
- [**Spark**](#spark): Kubernetes Pod for executing spark-submit jobs
- [**Localstack**](#localstack): Local environment that mimics AWS Cloud (S3, DynamoDB)
- [**Tensorflow**](#tensorflow): Kubernetes Pod for training and predicting with Tensorflow models