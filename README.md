# Machine Learning Stack
![release](https://img.shields.io/badge/release-v0.0.1-blue)
![Black Logo](https://img.shields.io/badge/code%20style-black-000000.svg)
> *Initial work! No promise on functionality or up to date documentation. Mostly a pet project*

It is common for data scientists to be well equipped in languages and packages commonly used for statistical analysis and modelling. It is less common that data scientits are equipped to properly implement those models at a production level while adhering to software engineering principles.

**ml-stack** provides a local development stack for data scientists that imitate production environments.


## Design
The design is in terms of the Kubernetes Pods. TODO: include Miniconda development with Jupyter and NVIDIA GPU support.

<p align="center">
    <img src='docs/design.png' width=700>
</p>


### Components
- [**Conda**](#conda): A minimal Anaconda environment for local development
- [**Docker / Kubernetes**](#kubernetes): Base images and Pod executables
- [**Spark**](#spark): Kubernetes Pod for executing spark-submit jobs
- [**Localstack**](#localstack): Local environment that mimics AWS Cloud (S3, DynamoDB)
- [**Tensorflow**](#tensorflow): Kubernetes Pod for training and predicting with Tensorflow models

### Volume Mounts
- **models**: Any directory, HD5, Protobuf, file to be trained or predicted with
- **scripts**: Scripts to execute. Each component will have a base script (see `build.tensorflow.model`), but additionals will also be persisted.
- **data**: Data to simulate in (for now only) localstack. These can be read via an S3Reader. Formats vary per component.


## Getting Started

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


### installing on ubuntu
```
then
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
    deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
    apt-get update
    apt-get install -y kubelet kubeadm kubectl
    apt-mark hold kubelet kubeadm kubectl
```

follow instructions for first apply and joining nodes.
```
kubectl taint nodes --all node-role.kubernetes.io/master-
```

