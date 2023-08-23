# Projeto WebSite em Vue.js

# Linux:

## Se nao tiver Python 2.x, execute o comando abaixo:

```
sudo apt install python2.7
```

## Verifique se a instalação foi realizada com sucesso:

```
python2.7 --version
```

## Crie um ambiente virtual:

```
virtualenv -p {caminhoDoPython2.7} {nomeDoAmbiente}
```

## Por padrão, o nome do ambiente pode ser chamado de venv.

## Por padrão, o caminho do python 2.7 é /usr/bin/python2.7, mas para saber o caminho do python2.7 pode ser executado o comando abaixo:

```
which python2.7
```

## Entre no ambiente da máquina virtual por meio do terminal da sua IDE:

```
cd venv
source ./bin/activate
```

## No ambiente virtual, execute os comandos abaixo para instalar e utilizar o node 8

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
nvm install 8
nvm use 8
```

## Instale as dependências do projeto:

```
npm install
```

### Compile o projeto para desenvolvimento:
```
npm run serve
```

### Compile o projeto para produção:
```
npm run build
```