# Será utilizado o Ubuntu 14.04 devido às limitações do mósulo node-sass 
# https://github.com/sass/node-sass/releases/tag/v4.14.1
FROM ubuntu:14.04

# Atualiza as dependências
RUN apt-get update && apt-get upgrade -y

# Instala Python 2.7
RUN apt-get install -y python2.7 
RUN apt-get install -y python-pip
RUN apt-get install -y python-setuptools 
RUN apt-get install -y curl
RUN apt-get install -y build-essential
RUN apt-get install -y python-virtualenv
RUN apt-get install -y dos2unix


WORKDIR /app
COPY . .

RUN cat entrypoint.sh

RUN dos2unix entrypoint.sh

RUN chmod +x entrypoint.sh && cat entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]