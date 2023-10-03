import os

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Double
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Despesa(Base):
    
    __tablename__ = 'f_despesa'
    __table_args__ = {'schema': os.environ.get('POSTGRES_SCHEMA')}
    
    cd_municipio = Column(String, ForeignKey("f_ibge.cd_municipio"), nullable=False)
    id_despesa_detalhe = Column("id_despesa_detalhe", Integer, nullable=False, primary_key=True)
    
    mes = Column("mes", Integer, nullable=False)
    mes_extenso = Column("mes_extenso", String, nullable=False)
    ano = Column("ano", Integer, nullable=False)
    cd_programa = Column("cd_programa", Integer, nullable=False)
    ds_programa = Column("ds_programa", String, nullable=False)
    cd_acao = Column("cd_acao", Integer, nullable=False)
    ds_acao = Column("ds_acao", String, nullable=False)
    ds_orgao = Column("ds_orgao", String, nullable=False)
    tp_despesa = Column(String, nullable=False)
    nr_empenho = Column(String, nullable=False)
    tp_identificador_despesa = Column(String, nullable=False)
    nr_identificador_despesa = Column(String, nullable=False)
    ds_despesa = Column(String, nullable=False)
    dt_emissao_despesa = Column(DateTime, nullable=False)
    vl_despesa = Column("vl_despesa", Double, nullable=False)
    ds_funcao_governo = Column(String, nullable=False)
    ds_subfuncao_governo = Column(String, nullable=False)
    ds_fonte_recurso = Column(String, nullable=False)
    ds_cd_aplicacao_fixo = Column(String, nullable=False)
    ds_modalidade_lic = Column(String, nullable=False)
    ds_elemento = Column(String, nullable=False)
    historico_despesa = Column(String, nullable=False)
    latitude = Column("latitude", String, nullable=True)
    longitude = Column("longitude", String, nullable=True)



class Ibge(Base):

    def __init__(self, cd_municipio, nome_municipio, populacao):
        self.cd_municipio = cd_municipio
        self.nome_municipio = nome_municipio
        self.populacao = populacao

    __tablename__ = 'f_ibge'
    __table_args__ = {'schema': os.environ.get('POSTGRES_SCHEMA')}

    cd_municipio = Column("cd_municipio", String, nullable=False, primary_key=True)
    nome_municipio = Column("nome_municipio", String, nullable=False)
    populacao = Column("populacao", Integer, nullable=False)

    despesa = relationship('Despesa', primaryjoin="Ibge.cd_municipio==Despesa.cd_municipio", backref='Ibge')