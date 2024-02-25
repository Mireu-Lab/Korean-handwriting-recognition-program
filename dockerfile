FROM nvidia/cuda:12.0.0-cudnn8-runtime-ubuntu22.04

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# Setup Program
RUN apt-get update &&\ 
    apt-get -y upgrade &&\
    mkdir -p /run/sshd &&\
    apt-get install -y sudo\
    vim\
    unzip\
    nano\ 
    wget\ 
    net-tools\ 
    git\
    openssh-server\
    python3\
    python3-pip

# User Setup
ENV PASSWORD "Hosting"

RUN useradd -ms /bin/bash -d /home/Hosting Hosting&&\
    usermod -aG sudo Hosting

RUN mkdir /home/Hosting/workspace &&\
    chmod 777 /home/Hosting/workspace

WORKDIR /home/Hosting/workspace
RUN ssh-keygen -A

CMD echo "Hosting":$PASSWORD | chpasswd && /usr/sbin/sshd -D
