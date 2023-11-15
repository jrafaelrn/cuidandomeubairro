#!/bin/bash

echo -e "\n...Iniciando o script..."
ls -lah
cd /app


# Checando ambiente Python
echo -e "...Checando ambiente Python...\nVersão = "
python2.7 --version

sleep 1
echo "Local = $(which python2.7)"
echo "PIP Versão = $(pip --version)"


python -c "import sys; is_64bits = sys.maxsize > 2**32; print('\nSistema 64 bits = {}\n'.format(is_64bits))"


echo -e "\n...Criando ambiente virtual...\n"
virtualenv -p $(which python2.7) venv

echo -e "\n...Ativando ambiente virtual...\n"
cd venv && source bin/activate && echo -e "\n...Ambiente virtual ativado!!!\n"
cd ..
pip install geojson

# Instala e configura a versão do Node.js
echo -e "\n...Instalando o NVM...\n"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

export NVM_DIR="$HOME/.nvm" 
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"


# Instala as dependências do Node.js
echo -e "\n...Instalando os pacotes do projeto...\n"
nvm install 12
nvm use 12
npm install


# Inicia o servidor Node.js
echo -e "\n...Iniciando o servidor...\n"
echo -e "Versão do Node.js = $(node --version)"
echo -e "Versão do NPM = $(npm --version)"

# To debug
#while sleep 1000; do :; done

# To run
npm run serve

#cp -r /root/.npm/_logs /app/