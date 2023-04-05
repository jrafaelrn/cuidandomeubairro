FROM ubuntu:latest

# Copy files
COPY ./import_layouts/states/rj/rio_de_janeiro ./app
COPY ./requirements.txt ./app
WORKDIR /app


# Update Linux environment and install packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3 python3-pip git


# Config Python environment
RUN pip install -r requirements.txt


RUN git clone https://github.com/okfn-brasil/gastos_abertos.git
RUN cd gastos_abertos


RUN python3 setup.py install

CMD ["flask", "run",]