FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

# Basic setting library
ENV DEBIAN_FRONTEND=noninteractive
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-key del 7fa2af80
RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

RUN apt-get update \
  && apt-get install --yes --no-install-recommends \
    sudo \
    git \
    tig \
    cmake \
    pkg-config \
    unzip \
    wget \
    build-essential \
    libssl-dev\
    libbz2-dev\
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    curl \
    libsm6 \
    libgtk2.0-dev \
    vim \
    less \
    pv \
    zlib1g-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    liblzma-dev \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Make sudo user
ARG USERNAME
RUN useradd ${USERNAME} -G sudo -s /bin/bash -m  && \
    echo ${USERNAME}' ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    chown ${USERNAME}:${USERNAME} /home/${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}
ENV HOME /home/${USERNAME}

# Install pyenv & install python
ENV PYTHON_VERSION 3.7.2
ENV PYENV_ROOT /home/${USERNAME}/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}

# Install python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip setuptools && \
    pip install -r /tmp/requirements.txt

# Install anaconda
WORKDIR /tmp
RUN curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
RUN bash Anaconda3-2020.07-Linux-x86_64.sh -b -p /home/${USERNAME}/anaconda3

RUN /home/${USERNAME}/anaconda3/bin/conda install -y pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch

ENV CUDA_HOME=/usr/local/cuda-10.2

# RUN /home/${USERNAME}/anaconda3/bin/conda install -c conda-forge nvidia-apex

# # Install nvidia/apex
# # https://github.com/NVIDIA/apex
WORKDIR /tmp
RUN git clone https://github.com/NVIDIA/apex && \
    cd apex && \
    git reset --hard 3fe10b5597ba14a748ebb271a6ab97c09c5701ac && \
    pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./


WORKDIR /home/${USERNAME}
# Install kaggle command
COPY kaggle_apikey.json /tmp/kaggle.json
RUN mkdir $HOME/.kaggle && \
    cp /tmp/kaggle.json $HOME/.kaggle/kaggle.json && \
    chmod 600 $HOME/.kaggle/kaggle.json

# Install fish shell
RUN sudo apt-get update && \
    sudo apt-get -y install software-properties-common && \
    sudo apt-add-repository ppa:fish-shell/release-3 && \
    sudo apt-get -y install fish && \
    curl https://git.io/fisher --create-dirs -sLo ~/.config/fish/functions/fisher.fish

# change the default shell
ENV SHELL /usr/bin/fish

# install your fish plugins
RUN /usr/bin/fish -c "fisher install oh-my-fish/theme-eclm jethrokuan/z 0rax/fish-bd oh-my-fish/plugin-peco"

# config and clean up
RUN sudo apt-get clean && sudo apt-get autoremove
