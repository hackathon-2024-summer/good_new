FROM phpmyadmin:5.1-apache
ARG PORT_PMA_FAST

# 2つのファイルのポート番号 80を環境変数で書き換え
RUN sed -i "s/80/${PORT_PMA_FAST}/" /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf
