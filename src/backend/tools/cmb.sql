CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS cmb;


CREATE TABLE IF NOT EXISTS cmb.f_ibge (
    cd_municipio character varying(10) NOT NULL,
    nome_municipio character varying(100) NOT NULL,
    populacao integer NOT NULL,
    PRIMARY KEY (cd_municipio)
);


CREATE TABLE IF NOT EXISTS cmb.f_despesa (
    mes integer NOT NULL,
    mes_extenso character varying(20) NOT NULL,
    ano integer NOT NULL,
    cd_programa character varying(30),
    ds_programa character varying(100),
    cd_acao character varying(30),
    ds_acao character varying(100),
    id_despesa_detalhe character varying(30) NOT NULL,
    ds_orgao character varying(100),
    tp_despesa character varying(30),
    nr_empenho character varying(30) NOT NULL,
    tp_identificador_despesa character varying(50),
    nr_identificador_despesa character varying(100),
    ds_despesa character varying(500),
    dt_emissao_despesa date NOT NULL,
    valor_despesa numeric(15,2) NOT NULL,
    ds_funcao_governo character varying(150),
    ds_subfuncao_governo character varying(150),
    ds_fonte_recurso character varying(150),
    ds_cd_aplicacao_fixo character varying(180),
    ds_modalidade_lic character varying(50),
    ds_elemento character varying(150),
    historico_despesa character varying(1000) NOT NULL,
    latitude character varying(50),
    longitude character varying(50),
    cd_municipio character varying(10) NOT NULL,
    CONSTRAINT fk_municipio
        FOREIGN KEY (cd_municipio)
            REFERENCES cmb.f_ibge (cd_municipio)
            ON UPDATE CASCADE,
    PRIMARY KEY (id_despesa_detalhe, cd_municipio)
);


CREATE MATERIALIZED VIEW IF NOT EXISTS tabela_info AS
	SELECT 	DESP.ds_funcao_governo, 
			SUM(DESP.valor_despesa) filter (where DESP.tp_despesa = 'Valor Pago') as planejado,
			SUM(DESP.valor_despesa) filter (where DESP.tp_despesa = 'Empenhado') as empenhado,
			SUM(DESP.valor_despesa) filter (where DESP.tp_despesa = 'Valor Liquidado') as liquidado,
			SUM(DESP.valor_despesa) filter (where DESP.tp_despesa = 'Anulação') as anulado,
			SUM(DESP.valor_despesa) filter (where DESP.tp_despesa = 'Reforço') as reforco
	FROM f_despesa AS DESP
	GROUP BY DESP.ds_funcao_governo


REFRESH MATERIALIZED VIEW tabela_info;