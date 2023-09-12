# Cuidando do Meu Bairro 2.1
Repositório para TCC - EACH-USP

## ❓ O que faz esse projeto?  

Adiciona os dados do [Tribunal de Contas do Estado de São Paulo (TCESP)](https://tce.sp.gov.br) relativos ao ano de 2.023 ao projeto [Cuidando do Meu Bairro (CMB) 2.0](https://cuidando.vc), permitindo a visualização no mapa das despesas públicas de diversos municípios do estado.<br>

## 📝 Como foi feito?
Para o *back-end* foi desenvolvido um *script* em Python que faz o *download* deste [arquivo de dados CSV do TCESP](https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2023.zip), processa-o e em seguida envia as informações para um banco de dados, que é utilizado pelo *front-end*.<br>
Esse *script* é executado automaticamente dentro de um container Docker e pode ser encontrado [aqui](./src/backend/run_etl_cmb.py).<br>

O *front-end* foi adaptado a partir dos seguintes repositórios:
- Projeto base do CMB disponível no [GitLab](https://gitlab.com/cuidandodomeubairro/website-vuejs) com os principais elementos da página, com o objetivo de manter a experiência de uso próxima à plataforma do CMB já existente.
- Atualização de pacotes e *script* de execução desenvolvido por Silas B. Reis e disponível no [GitLab](https://gitlab.com/cuidandodomeubairro/website-vuejs/-/commit/6570c5b6d5c7024f78e5bc2b692ced7184f189b2) através da branch `projeto-executavel`.
  - A partir desse *script* de execução, foram realizadas 2 alterações:
    1. Atualização da versão do `node` para 12
    2. Adição do pacote `leaflet` na versão 1.7.1


## 🕙 O que preciso fazer antes de iniciar o projeto?
Requisitos mínimos:
- Docker e Docker Compose
- 10 GB de espaço livre em disco
- ~~Tempo...~~


## ▶️ E para executar?

Clone o repositório:
```bash
git clone https://github.com/jrafaelrn/cuidandomeubairro.git
```

Acesse a pasta do projeto:
```bash
cd cuidandomeubairro
```

Atualize as variáveis de ambiente no arquivo `.env`<br>
>> Para dúvidas em como obter as chaves de API do Telegram, consulte a documentação oficial [clicando aqui.](https://core.telegram.org/bots/features#botfather)<br>

Execute o comando:
```bash
docker-compose up
```

*OBS: A primeira vez que o container do Nominatim for executado, ele irá baixar os dados do OpenStreetMap, o que pode demorar mais de 2..3 horas, dependendo da sua conexão com a internet e do seu computador.*

## ✅ Se você deu sorte, então...
Acesse o endereço http://localhost:8080 no seu navegador e veja o CMB em ação!<br><br>

## 💻 E se eu quiser desenvolver/debugar?
Para isso foi criado o arquivo [devcontainer.json](./.devcontainer/devcontainer.json), que serve como base para o VS Code criar todo o ambiente de desenvolvimento e ser executado a partir do container Docker.<br>
Por padrão, o VS Code abre o projeto do *front-end*, mas isso pode ser alterado no arquivo [devcontainer.json](./.devcontainer/devcontainer.json) na propriedade `service`.<br>
Para mais informações, confira a documentação oficial [clicando aqui.](https://code.visualstudio.com/docs/devcontainers/containers)