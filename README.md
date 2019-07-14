# Data Science Stack
It is common for data scientists to be well equipped in languages and packages commonly used for statistical analysis and modelling. It is less common that data scientits are equipped to properly implement those models at a production level while adhering to software engineering principles.

**ds-stack** provides a local development stack for data scientists that imitate production environments.

## Setup
Initial versions assume an install of Ubuntu 16.04 LTS with an NVIDIA GPU.

```sh
sudo ./setup.sh
```

### Dependencies
Initial versions assume that you have **Ubuntu 16.04** as your operating system. Later versions may include other operating systems, GPU/non-gpu support, and dynamic OS checks.

## Design
<br>

<p align="center">
    <img src='docs/design.png' height=300>
</p>

### Components
- [**Conda**](#conda): A minimal Anaconda environment for local development
- [**Docker / Kubernetes**](#kubernetes): Base images and Pod executables
- [**Spark**](#spark): Kubernetes Pod for executing spark-submit jobs
- [**Localstack**](#localstack): Local environment that mimics AWS Cloud (S3, DynamoDB)
