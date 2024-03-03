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
        python3.11-dev \
        python3.11-venv \
        python3.11-distutils \
        python3.10-dev \
        python3.10-venv \
        python3.10-distutils \
        python3.9-dev \
        python3.9-venv \
        python3.9-distutils \
        python3.8-dev \
        python3.8-venv \
        python3.8-distutils
    && rm -rf /var/lib/apt/lists/*

# install pip
RUN echo "\n${CYAN}INSTALL PIP${CLEAR}"; \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    pip3.11 install --upgrade pip && \
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
COPY ./config/henanigans.zsh-theme .oh-my-zsh/custom/themes/henanigans.zsh-theme

ENV LANG "C.UTF-8"
ENV LANGUAGE "C.UTF-8"
ENV LC_ALL "C.UTF-8"
# ------------------------------------------------------------------------------

FROM base AS dev

USER ubuntu
WORKDIR /home/ubuntu

# install dev dependencies
RUN echo "\n${CYAN}INSTALL DEV DEPENDENCIES${CLEAR}"; \
    curl -sSL \
        https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py \
        | python3.11 - && \
    pip3.11 install --upgrade --user \
        pdm \
        'pdm-bump<0.7.0' \
        'rolling-pin>=0.9.2' && \
    mkdir -p /home/ubuntu/.oh-my-zsh/custom/completions && \
    pdm self update --pip-args='--user' && \
    pdm completion zsh > /home/ubuntu/.oh-my-zsh/custom/completions/_pdm

# setup pdm
COPY --chown=ubuntu:ubuntu config/build.yaml /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/dev.lock /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/pdm.toml /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/prod.lock /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu config/pyproject.toml /home/ubuntu/config/
COPY --chown=ubuntu:ubuntu scripts/x_tools.sh /home/ubuntu/scripts/
RUN echo "\n${CYAN}SETUP DIRECTORIES${CLEAR}"; \
    mkdir pdm

# create dev env
WORKDIR /home/ubuntu/pdm
RUN echo "\n${CYAN}INSTALL DEV ENVIRONMENT${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
    x_env_init dev 3.11 && \
    cd /home/ubuntu && \
    ln -s `_x_env_get_path dev 3.11` .dev-env && \
    ln -s `_x_env_get_path dev 3.11`/lib/python3.11/site-packages .dev-packages

# create prod envs
RUN echo "\n${CYAN}INSTALL PROD ENVIRONMENTS${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
    x_env_init prod 3.11 && \
    x_env_init prod 3.10 && \
    x_env_init prod 3.9 && \
    x_env_init prod 3.8

# build jupyter lab
RUN echo "\n${CYAN}BUILD JUPYTER LAB${CLEAR}"; \
    . /home/ubuntu/scripts/x_tools.sh && \
    export CONFIG_DIR=/home/ubuntu/config && \
    export SCRIPT_DIR=/home/ubuntu/scripts && \
    x_env_activate_dev && \
    jupyter lab build

WORKDIR /home/ubuntu

# cleanup dirs
RUN echo "\n${CYAN}REMOVE DIRECTORIES${CLEAR}"; \
    rm -rf /home/ubuntu/config /home/ubuntu/scripts

ENV REPO='jupyterlab_henanigans'
ENV PYTHONPATH ":/home/ubuntu/$REPO/python:/home/ubuntu/.local/lib"
ENV PYTHONPYCACHEPREFIX "/home/ubuntu/.python_cache"
ENV HOME /home/ubuntu
ENV JUPYTER_RUNTIME_DIR /tmp/jupyter_runtime

