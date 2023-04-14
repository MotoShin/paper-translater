# ベースとなる docker image
ARG python_version=3.11
FROM python:${python_version}

# コンテナ内でコマンドを実行するユーザの設定
# コンテナ内ではdockerユーザでコマンド実行することになる
ARG username=docker
ARG useruid=1000
ARG usergid=${useruid}

# 最低限installしておいた方がいいやつ
RUN apt-get -y update && apt-get upgrade -qqy && apt-get -y install \
    sudo \
    bash \
    git \
    vim

RUN pip install --upgrade setuptools

# dockerユーザの作成
RUN groupadd --gid ${usergid} ${username} && \
    useradd -s /bin/bash --uid ${useruid} --gid ${usergid} -m ${username} && \
    echo ${username}' ALL=NOPASSWD: ALL' >> /etc/sudoers

# dockerユーザに切り替え
USER ${username}
WORKDIR /home/${username}/paper-translater

COPY . /home/${username}/paper-translater
