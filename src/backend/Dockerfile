FROM ubuntu:22.04

# Update Linux environment and install packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install git
RUN apt-get -y install postgresql-client
RUN apt-get -y install libpq5
RUN apt install -qq --assume-yes mesa-utils libgl1-mesa-glx libxcursor1 libxrandr2 libxxf86vm1 x11-xserver-utils xfonts-base xserver-common dos2unix
RUN apt install -y net-tools
RUN apt install -y lsof

# Set the working directory and copy files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Isola o entrypoint.sh por conta da incompatibilidade de quebra de linha entre Windows e Linux
RUN mkdir /entry
COPY ./entrypoint.sh /entry/entrypoint.sh
RUN dos2unix /entry/entrypoint.sh
RUN chmod +x /entry/entrypoint.sh


# Run the application
ENTRYPOINT ["/entry/entrypoint.sh"]