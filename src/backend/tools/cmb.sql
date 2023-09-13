
CREATE TABLE IF NOT EXISTS d_programa (
    cd_programa integer NOT NULL,
    ds_programa character varying(100) NOT NULL,
    PRIMARY KEY (cd_programa)
);

CREATE TABLE IF NOT EXISTS d_acao (
    cd_acao integer NOT NULL,
    ds_acao character varying(100) NOT NULL,
    PRIMARY KEY (cd_acao)
);

CREATE TABLE IF NOT EXISTS d_municipio (
    cd_municipio integer NOT NULL,
    ds_municipio character varying(100) NOT NULL,
    PRIMARY KEY (cd_municipio)
);

CREATE TABLE IF NOT EXISTS d_calendario (
    data date NOT NULL,
    dia integer NOT NULL,
    mes integer NOT NULL,
    ano integer NOT NULL,
    mes_extenso character varying(100) NOT NULL,
    PRIMARY KEY (data)
);

CREATE TABLE IF NOT EXISTS f_despesa (
    cd_programa integer NOT NULL,
    cd_acao integer NOT NULL,
    cd_municipio integer NOT NULL,
    id_despesa_detalhe integer NOT NULL,
    ds_orgao character varying(100) NOT NULL,
    tp_despesa character varying(30) NOT NULL,
    nr_identificador_despesa character varying(100) NOT NULL,
    ds_despesa character varying(100) NOT NULL,
    dt_emissao_despesa date NOT NULL,
    vl_despesa numeric(15,2) NOT NULL,
    ds_funcao_governo character varying(50) NOT NULL,
    ds_subfuncao_governo character varying(50) NOT NULL,
    ds_fonte_recurso character varying(50) NOT NULL,
    ds_cd_aplicacao_fixo character varying(50) NOT NULL,
    ds_modalidade_lic character varying(50) NOT NULL,
    ds_elemento character varying(50) NOT NULL,
    historico_despesa character varying(500) NOT NULL,
    PRIMARY KEY (id_despesa_detalhe, cd_municipio),
    CONSTRAINT cd_programa_fkey 
        FOREIGN KEY (cd_programa)
        REFERENCES d_programa (cd_programa),
    CONSTRAINT cd_acao_fkey 
        FOREIGN KEY (cd_acao)
        REFERENCES d_acao (cd_acao),
    CONSTRAINT cd_municipio_fkey
        FOREIGN KEY (cd_municipio)
        REFERENCES d_municipio (cd_municipio)
);