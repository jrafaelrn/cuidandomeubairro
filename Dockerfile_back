FROM ubuntu:14.04

ARG PYTHON_VERSION=2.7.9

# Install dependencies
RUN apt-get update \
  && apt-get install -y wget gcc make openssl libffi-dev libgdbm-dev libsqlite3-dev libssl-dev zlib1g-dev \
  && apt-get clean

WORKDIR /tmp/


# Build Python from source
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz \
  && tar --extract -f Python-$PYTHON_VERSION.tgz \
  && cd ./Python-$PYTHON_VERSION/ \
  && ./configure --with-ensurepip=install --enable-optimizations --prefix=/usr/local \
  && make && make install \
  && cd ../ \
  && rm -r ./Python-$PYTHON_VERSION*


# Copy files
#COPY ./import_layouts/states/rj/rio_de_janeiro ./app
WORKDIR /app
#COPY ./import_layouts/states/sp/sao_paulo ./
#COPY ./requirements.txt ./
#RUN chmod +x /app/entrypoint.sh



# Update Linux environment and install packages
RUN apt-get -y update
RUN apt-get -y upgrade
#RUN apt-get -y install python3
RUN apt-get -y install python-pip
RUN apt-get -y install git
RUN apt-get -y install postgresql-client
RUN apt-get -y install libpq5


# Config Python environment
RUN python --version 
RUN pip install -r requirements.txt


# Run the application
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]