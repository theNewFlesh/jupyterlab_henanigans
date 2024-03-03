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
        --gid $GID_ ubuntu && \
    usermod -aG root ubuntu

# setup sudo
RUN echo "\n${CYAN}SETUP SUDO${CLEAR}"; \
    apt update && \
    apt install -y sudo && \
    usermod -aG sudo ubuntu && \
    echo '%ubuntu    ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu

# update ubuntu and install basic dependencies
RUN echo "\n${CYAN}INSTALL GENERIC DEPENDENCIES${CLEAR}"; \
    apt update && \
    apt install -y \
        apt-transport-https \
        bat \
        btop \
        ca-certificates \
        curl \
        exa \
        git \
        gnupg \
        graphviz \
        jq \
        parallel \
        ripgrep \
        software-properties-common \
        unzip \
        vim \
        wget && \
    rm -rf /var/lib/apt/lists/*

# install yq
RUN echo "\n${CYAN}INSTALL YQ${CLEAR}"; \
    curl -fsSL \
        https://github.com/mikefarah/yq/releases/download/v4.9.1/yq_linux_amd64 \
        -o /usr/local/bin/yq && \
    chmod +x /usr/local/bin/yq

# install all python versions
RUN echo "\n${CYAN}INSTALL PYTHON${CLEAR}"; \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y \
        python3-pydot \
        python3.10-dev \
        python3.10-venv \
        python3.10-distutils \
    && rm -rf /var/lib/apt/lists/*

# install pip
RUN echo "\n${CYAN}INSTALL PIP${CLEAR}"; \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.10 get-pip.py && \
    pip3.10 install --upgrade pip && \
    rm -rf get-pip.py

# install nodejs (needed by jupyter lab)
RUN echo "\n${CYAN}INSTALL NODEJS${CLEAR}"; \
    sudo mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    export NODE_VERSION=18 && \
    echo "deb \
        [signed-by=/etc/apt/keyrings/nodesource.gpg] \
        https://deb.nodesource.com/node_$NODE_VERSION.x \
        nodistro main" \
        | sudo tee /etc/apt/sources.list.d/nodesource.list && \
    sudo apt update && \
    sudo apt install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# install and setup zsh
RUN echo "\n${CYAN}SETUP ZSH${CLEAR}"; \
    apt update && \
    apt install -y zsh && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh \
        -o install-oh-my-zsh.sh && \
    echo y | sh install-oh-my-zsh.sh && \
    mkdir -p /root/.oh-my-zsh/custom/plugins && \
    cd /root/.oh-my-zsh/custom/plugins && \
    git clone https://github.com/zdharma-continuum/fast-syntax-highlighting && \
    git clone https://github.com/zsh-users/zsh-autosuggestions && \
    npm i -g zsh-history-enquirer --unsafe-perm && \
    cd /home/ubuntu && \
    cp -r /root/.oh-my-zsh /home/ubuntu/ && \
    chown -R ubuntu:ubuntu .oh-my-zsh && \
    rm -rf install-oh-my-zsh.sh && \
    echo 'UTC' > /etc/timezone


USER ubuntu
ENV PATH="/home/ubuntu/.local/bin:$PATH"
# COPY ./config/henanigans.zsh-theme .oh-my-zsh/custom/themes/henanigans.zsh-theme

ENV LANG "C.UTF-8"
ENV LANGUAGE "C.UTF-8"
ENV LC_ALL "C.UTF-8"
# ------------------------------------------------------------------------------

FROM base AS dev

USER ubuntu
WORKDIR /home/ubuntu

# install python dependencies
COPY ./dev_requirements.txt dev_requirements.txt
COPY ./prod_requirements.txt prod_requirements.txt
# RUN echo "\n${CYAN}INSTALL PYTHON DEPENDECIES${CLEAR}"; \
#     pip3.10 install -r dev_requirements.txt && \
#     pip3.10 install -r prod_requirements.txt && \
#     sudo /home/ubuntu/.local/bin/jupyter server extension enable --py jupyterlab_git

# # build jupyter lab
# RUN echo "\n${CYAN}BUILD JUPYTER LAB${CLEAR}"; \
#     . /home/ubuntu/scripts/x_tools.sh && \
#     export CONFIG_DIR=/home/ubuntu/config && \
#     export SCRIPT_DIR=/home/ubuntu/scripts && \
#     x_env_activate_dev && \
#     jupyter lab build

# # cleanup dirs
# RUN echo "\n${CYAN}REMOVE DIRECTORIES${CLEAR}"; \
#     rm -rf /home/ubuntu/config /home/ubuntu/scripts

ENV REPO='jupyterlab_henanigans'
ENV PYTHONPATH ":/home/ubuntu/$REPO/python:/home/ubuntu/.local/lib"
ENV PYTHONPYCACHEPREFIX "/home/ubuntu/.python_cache"
ENV HOME /home/ubuntu
ENV JUPYTER_RUNTIME_DIR /tmp/jupyter_runtime

