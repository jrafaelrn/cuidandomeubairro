CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS cmb;

CREATE TABLE IF NOT EXISTS cmb.f_despesa (
    mes integer NOT NULL,
    mes_extenso character varying(20) NOT NULL,
    ano integer NOT NULL,
    cd_programa character NOT NULL,
    ds_programa character varying(100) NOT NULL,
    cd_acao character NOT NULL,
    ds_acao character varying(100) NOT NULL,
    cd_municipio character NOT NULL,
    id_despesa_detalhe character NOT NULL,
    ds_orgao character varying(100) NOT NULL,
    tp_despesa character varying(30) NOT NULL,
    nr_empenho character varying(50) NOT NULL,
    tp_identificador_despesa character varying(50) NOT NULL,
    nr_identificador_despesa character varying(100) NOT NULL,
    ds_despesa character varying(500) NOT NULL,
    dt_emissao_despesa date NOT NULL,
    vl_despesa numeric(15,2) NOT NULL,
    ds_funcao_governo character varying(150) NOT NULL,
    ds_subfuncao_governo character varying(150) NOT NULL,
    ds_fonte_recurso character varying(150) NOT NULL,
    ds_cd_aplicacao_fixo character varying(180) NOT NULL,
    ds_modalidade_lic character varying(50) NOT NULL,
    ds_elemento character varying(150) NOT NULL,
    historico_despesa character varying(1000) NOT NULL,
    localizacao geography(Point,4326),
    latitude character varying(50),
    longitude character varying(50),
    PRIMARY KEY (id_despesa_detalhe, cd_municipio)
);


CREATE TABLE IF NOT EXISTS cmb.f_ibge (
    cd_municipio integer NOT NULL,
    nome_municipio character varying(100) NOT NULL,
    populacao integer NOT NULL,
    PRIMARY KEY (cd_municipio)
);