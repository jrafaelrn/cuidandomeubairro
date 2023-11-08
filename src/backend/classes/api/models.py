import os

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Double, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Despesa(Base):
    
    __tablename__ = 'f_despesa'
    __table_args__ = {'schema': os.environ.get('POSTGRES_SCHEMA')}
    
    cd_municipio: Mapped[str] = mapped_column("cd_municipio", String(), nullable=False, primary_key=True)
    id_despesa_detalhe: Mapped[str] = mapped_column("id_despesa_detalhe", String(), nullable=False, primary_key=True)
    
    mes: Mapped[int] = mapped_column("mes", Integer(), nullable=False)
    mes_extenso: Mapped[str] = mapped_column("mes_extenso", String(), nullable=False)
    ano: Mapped[int] = mapped_column("ano", Integer(), nullable=False)
    cd_programa: Mapped[str] = mapped_column("cd_programa", String())
    ds_programa: Mapped[str] = mapped_column("ds_programa", String())
    cd_acao: Mapped[str] = mapped_column("cd_acao", String())
    ds_acao: Mapped[str] = mapped_column("ds_acao", String())
    ds_orgao: Mapped[str] = mapped_column("ds_orgao", String())
    tp_despesa: Mapped[str] = mapped_column("tp_despesa", String())
    nr_empenho: Mapped[str] = mapped_column("nr_empenho", String())
    tp_identificador_despesa: Mapped[str] = mapped_column("tp_identificador_despesa", String(), nullable=True)
    nr_identificador_despesa: Mapped[str] = mapped_column("nr_identificador_despesa", String(), nullable=True)
    ds_despesa: Mapped[str] = mapped_column("ds_despesa", String(), nullable=True)
    dt_emissao_despesa: Mapped[datetime] = mapped_column("dt_emissao_despesa", DateTime(), nullable=False)
    valor_despesa: Mapped[float] = mapped_column("valor_despesa", Double(), nullable=False)
    ds_funcao_governo: Mapped[str] = mapped_column("ds_funcao_governo", String(), nullable=True)
    ds_subfuncao_governo: Mapped[str] = mapped_column("ds_subfuncao_governo", String(), nullable=True)
    ds_fonte_recurso: Mapped[str] = mapped_column("ds_fonte_recurso", String(), nullable=True)
    ds_cd_aplicacao_fixo: Mapped[str] = mapped_column("ds_cd_aplicacao_fixo", String(), nullable=True)
    ds_modalidade_lic: Mapped[str] = mapped_column("ds_modalidade_lic", String(), nullable=True)
    ds_elemento: Mapped[str] = mapped_column("ds_elemento", String(), nullable=True)
    historico_despesa: Mapped[str] = mapped_column("historico_despesa", String(), nullable=False)
    latitude: Mapped[str] = mapped_column("latitude", String(), nullable=True)
    longitude: Mapped[str] = mapped_column("longitude", String(), nullable=True)



class Ibge(Base):

    def __init__(self, cd_municipio, nome_municipio, populacao):
        self.cd_municipio = cd_municipio
        self.nome_municipio = nome_municipio
        self.populacao = populacao

    __tablename__ = 'f_ibge'
    __table_args__ = {'schema': os.environ.get('POSTGRES_SCHEMA')}

    cd_municipio: Mapped[str] = mapped_column("cd_municipio", String, nullable=False, primary_key=True)
    nome_municipio: Mapped[str] = mapped_column("nome_municipio", String, nullable=False)
    populacao: Mapped[int] = mapped_column("populacao", Integer, nullable=False)

    #despesa = relationship('Despesa', primaryjoin="Ibge.cd_municipio==Despesa.cd_municipio", backref='Ibge')


class TableInfo(Base):

    def __init__(self, engine):
        Base.metadata.reflect(bind=engine, views=True)

    __tablename__ = 'tabela_info'
    __table_args__ = {'schema': os.environ.get('POSTGRES_SCHEMA')}
    #__table__ = Table('tabela_info', Base.metadata,
    #                Column('ds_funcao_governo', String(), primary_key=True),
    #                Column('planejado', Double()),
    #                Column('empenhado', Double()),
    #                Column('liquidado', Double()),
    #                Column('anulado', Double()),
    #                Column('reforco', Double()),
    #                extend_existing=True
    #                )

    ds_funcao_governo: Mapped[str] = mapped_column("ds_funcao_governo", String(), nullable=False, primary_key=True)
    planejado: Mapped[float] = mapped_column("planejado", Double(), nullable=True)
    empenhado: Mapped[float] = mapped_column("empenhado", Double(), nullable=True)
    liquidado: Mapped[float] = mapped_column("liquidado", Double(), nullable=True)