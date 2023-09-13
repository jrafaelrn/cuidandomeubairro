FROM ubuntu:22.04

# Update Linux environment and install packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install git
RUN apt-get -y install postgresql-client
RUN apt-get -y install libpq5


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pwd && ls -lah

# Run the application
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]