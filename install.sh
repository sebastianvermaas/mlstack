#!/bin/bash

echo "        _      _           _     "
echo "  _ __ | |  __| |_ __ _ __| |__  "
echo " | '  \| | (_-<  _/ _  / _| / / "
echo " |_|_|_|_| /__/\__\__,_\__|_\_\ "
echo
echo "Welcome to Machine Learning Stack!"

apt update
apt upgrade -yy
apt autoremove -yy
apt-get update && apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
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
echo "---------------------------------"
echo "Installing Docker and Kubernetes "
echo "---------------------------------"
if [ -x "$(command version kubectl)" ]
else
    echo "Kubernetes already installed!"
fi


