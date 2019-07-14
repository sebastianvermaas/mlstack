#!/bin/bash
echo "  __        __              __       "
echo " /  )__/_  (  _ '_   _ _   ( _/_ _ / "
echo "/(_/(//(/ __)( /(-/)( (-  __)/(/( /( "
echo
echo "Setting up your data science stack"
echo

apt update
apt upgrade -yy
apt autoremove -yy

# Install Miniconda and ds conda environment
echo "----------------------------"
echo "Installing Miniconda"
echo "----------------------------"

if [ -x "$(command -v conda)" ]
then
    cd /tmp
    curl -O https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh
    sha256sum Miniconda3-4.6.14-Linux-x86_64.sh
    sh ./Miniconda3-4.6.14-Linux-x86_64.sh
else
    echo "Conda already installed!"
fi
export PATH=$HOME/miniconda3/bin:$PATH

# Install dependencies
echo "----------------------------"
echo "Setting up conda environment"
echo "----------------------------"

apt install python-opencv -yy
conda update -n base -c defaults conda -yy
conda env create -f conda.yml -yy

# Install Docker
echo "----------------------------"
echo "Installing Docker"
echo "----------------------------"

if [ -x "$(command version docker)" ]
then
    apt install containerd docker.io -yy
    apt install docker-ce docker-ce-cli containerd.io -yy
else
    echo "Docker already installed!"
fi

echo "Pulling Docker images..."
echo
echo "**Pulling Tensorflow image**"
docker pull tensorflow/tensorflow

echo "**Pulling Tensorflow 2.0 image**"
docker pull tensorflow/tensorflow

# Install Kubernetes
echo "----------------------------"
echo "Installing Kubernetes"
echo "----------------------------"
if [ -x "$(command version kubectl)" ]
then
    apt apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
    apt install -yy kubectl
else
    echo "Kubernetes already installed!"
fi


