FROM python:3.11

RUN apt-get update && apt-get install -y mariadb-client

# 言語・地域情報
RUN apt-get update && apt-get install -y sudo locales tree && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y --no-install-recommends \
  fonts-ipafont-gothic \
  fonts-ipafont-mincho
RUN apt-get install zsh -y  
RUN apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TERM xterm
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# コンテナ内に開放するポート。docker-compose.ymlと一致させる。
ARG PORT_FAST
EXPOSE $PORT_FAST

#ルート権限で操作するフォルダ /appを選択
WORKDIR /app
# コンテナのpythonライブラリをリスト化したrequirements.txtをlocalhostからコンテナ内にコピー。
# 使用したいライブラリがあれば事前にrequirements.txtを更新しておく。
COPY requirements.txt /app/

# requirements.txtに基づいてpython環境をコンテナ内に構築。
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install python-dotenv
RUN pip install -r requirements.txt

ENV PATH="/home/appuser/back/apis:${PATH}"

# localhostでid $whoamiを実行しuidとgidの数値を事前に確認し.envファイルに転機すること。
# localhostのユーザーと同一のuid・gidのユーザーを作成。
# localhostとコンテナ内が同一ユーザー扱いとなりGitの監視が混乱しない。
ARG MY_UID
ARG MY_GID

RUN if ! grep -q ":x:$MY_GID:" /etc/group; then groupadd -g $MY_GID appgroup; fi && \
  if ! grep -q ":x:$MY_UID:" /etc/passwd; then useradd --uid $MY_UID --gid $MY_GID --create-home appuser; fi

# dockerの仕様変更なのか、コンテナはroot権限で完成させねばならなくなったのかも。
# パスワード無しでroot権限をappuserにも付与する。
RUN usermod -aG sudo appuser
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN mkdir /home/appuser/back && chown appuser:appgroup /home/appuser/back
WORKDIR /home/appuser/back

# docker環境構築時などサーバー以外の常駐プロセスを起動させる。
# docker環境ができればコメントアウトする
# ENTRYPOINT ["/bin/sh", "-c"]
# CMD ["tail -f /dev/null"]