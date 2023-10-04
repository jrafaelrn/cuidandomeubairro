from dataclasses import dataclass, field
from datetime import datetime

# Colunas conforme o Banco de Dados

@dataclass()
class Despesa:

    cd_programa: str = field(init=False, default="")
    ds_programa: str = field(init=False, default="")
    cd_acao: str = field(init=False, default="")
    ds_acao: str = field(init=False, default="")
    cd_municipio: str = field(init=False, default="")
    id_despesa_detalhe: str = field(init=False, default="")
    ds_orgao: str = field(init=False, default="")
    tp_despesa: str = field(init=False, default="")
    nr_empenho: str = field(init=False, default="")
    tp_identificador_despesa: str = field(init=False, default="")
    nr_identificador_despesa: str = field(init=False, default="")
    ds_despesa: str = field(init=False, default="")
    dt_emissao_despesa: datetime = field(init=False, default=datetime(1900, 1, 1))
    valor_despesa: float = field(init=False, default=0.0)
    ds_funcao_governo: str = field(init=False, default="")
    ds_subfuncao_governo: str = field(init=False, default="")
    ds_fonte_recurso: str = field(init=False, default="")
    ds_cd_aplicacao_fixo: str = field(init=False, default="")
    ds_modalidade_lic: str = field(init=False, default="")
    ds_elemento: str = field(init=False, default="")
    historico_despesa: str = field(init=False, default="")
    mes: int = field(init=False, default=0)
    ano: int = field(init=False, default=0)
    mes_extenso: str = field(init=False, default="")
    latitude: str = field(init=False, default="")
    longitude: str = field(init=False, default="")