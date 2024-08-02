FROM mysql:8.0.32
ARG PORT_MYSQL_FAST
ARG MYSQL_USER
# my.cnf をコンテナにコピー
COPY ./my.cnf /etc/mysql/conf.d/my.cnf

# port を環境変数で書き換え
RUN sed -i "s|port =.*|port = ${PORT_MYSQL_FAST}|" /etc/mysql/conf.d/my.cnf 

# init.sql をコンテナにコピー
COPY ./init.sql /docker-entrypoint-initdb.d

# userを環境変数で書き換え
RUN sed -i "s|placeholder|${MYSQL_USER}|" /docker-entrypoint-initdb.d/init.sql
