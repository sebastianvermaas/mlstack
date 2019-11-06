# Machine Learning Stack
![release](https://img.shields.io/badge/release-v0.0.1-blue)
![Black Logo](https://img.shields.io/badge/code%20style-black-000000.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](
://opensource.org/licenses/MIT)

It is common for data scientists to be well equipped in languages and packages commonly used for statistical analysis and modeling. It is less common that data scientists are equipped to properly implement those models in production pipelines.

**MLStack** provides a toolkit for Data Scientists to develop production-level modules in their local development environment.


## Design
<br>
<br>

<p align="center">
    <img src='docs/design.png' width=700>
</p>

<br>

MLStack provides two toolkits with shared dependencies:

- **Conda environment** - An Anaconda environment with common ML python libraries
- **Kubernetes cluster** - A Kubernetes cluster with common ML components


## Getting Started
### Prerequisites
MLStack assumes that you have [Docker](#https://docs.docker.com/) (19.03), [Kubernetes](#https://kubernetes.io/docs/home/) (1.16), and [Conda](#https://docs.conda.io/en/latest/) (4.7) installed. Installation instructions are not given as differents operating systems and environments require specific configuration.

### Install
MLStack can be installed with the following. Note that the setup will take some time as Docker images are pulled and/or built. So grab a cup of :coffee: and relax! (or read logs .. or both)

```sh
# Clone into the repository
git clone https://github.com/sebastianvermaas/mlstack.git
cd mlstack

# Install the Python library and CLI
pip install -e .

# Setup command for preparing Docker images
mlstack setup

```


## Usage
### Building specific images

```
mlstack build all
mlstack build airflow --requirements requirements.txt


mlstack deploy all
mlstack deploy spark --volumemount my-mount --hostpath path/to/my/host




mlstack close
mlstack upload


mlstack create bucket mybucket
mlstack upload data --bucket mybucket
