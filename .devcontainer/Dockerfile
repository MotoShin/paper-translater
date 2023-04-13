# ベースとなる docker image
ARG python_version=3.11
FROM python:${python_version}

# コンテナ内でコマンドを実行するユーザの設定
# コンテナ内ではvscodeユーザでコマンド実行することになる
ARG username=vscode
ARG useruid=1000
ARG usergid=${useruid}

# 最低限installしておいた方がいいやつ
RUN apt-get -y update && apt-get upgrade -qqy && apt-get -y install \
    sudo \
    bash \
    git \
    vim

RUN pip install --upgrade setuptools

# vscodeユーザの作成
RUN groupadd --gid ${usergid} ${username} && \
    useradd -s /bin/bash --uid ${useruid} --gid ${usergid} -m ${username} && \
    echo ${username}' ALL=NOPASSWD: ALL' >> /etc/sudoers

# vscodeユーザに切り替え
USER ${username}
WORKDIR /home/${username}

# フォーマッターのinstall
RUN pip install black
