FROM ubuntu:22.04 AS base

USER root

# coloring syntax for headers
ENV CYAN='\033[0;36m'
ENV CLEAR='\033[0m'
ENV DEBIAN_FRONTEND='noninteractive'

# setup ubuntu user
ARG UID_='1000'
ARG GID_='1000'
RUN echo "\n${CYAN}SETUP UBUNTU USER${CLEAR}"; \
    addgroup --gid $GID_ ubuntu && \
    adduser \
        --disabled-password \
        --gecos '' \
        --uid $UID_ \
        --gid $GID_ ubuntu
WORKDIR /home/ubuntu

# update ubuntu and install basic dependencies
RUN echo "\n${CYAN}INSTALL GENERIC DEPENDENCIES${CLEAR}"; \
    apt update && \
    apt install -y \
        software-properties-common \
        wget && \
    rm -rf /var/lib/apt/lists/*

# install python3.11 and pip
RUN echo "\n${CYAN}SETUP PYTHON3.11${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install --fix-missing -y python3.11 && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    rm -rf /home/ubuntu/get-pip.py

# install jupyterlab_henanigans
USER ubuntu
ENV REPO='jupyterlab_henanigans'
ENV PYTHONPATH "${PYTHONPATH}:/home/ubuntu/$REPO/python"
RUN echo "\n${CYAN}INSTALL JUPYTERLAB_HENANIGANS{CLEAR}"; \
    pip3.11 install --user --upgrade jupyterlab_henanigans

ENV PATH=$PATH:/home/ubuntu/.local/bin
