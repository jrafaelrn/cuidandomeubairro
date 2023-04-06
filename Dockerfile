FROM ubuntu:latest

# Copy files
#COPY ./import_layouts/states/rj/rio_de_janeiro ./app
COPY ./import_layouts/states/sp/sao_paulo ./app
COPY ./requirements.txt ./app
COPY ./entrypoint.sh ./app
RUN chmod +x /app/entrypoint.sh


# Update Linux environment and install packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3 python3-pip git


WORKDIR /app

# Config Python environment
RUN pip install -r requirements.txt

#RUN git clone https://github.com/okfn-brasil/gastos_abertos.git
RUN git clone https://github.com/okfn-brasil/gastos_abertos_dados.git



# Run the application
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
