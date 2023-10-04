import logging
import pandas as pd
import datetime
import os
import multiprocessing as mp
import time

from classes.city.city import City
from classes.extractor.extractor import Extractor
from multiprocessing import Process
from tqdm import tqdm

log = logging.getLogger(__name__)


class Extractor_tce(Extractor):
    
    def __init__(self):
        super().__init__(unzip=True, split_format='csv')
    
    
    def get_last_update(self):
        return datetime.datetime.now()
        

    def download(self):
        
        urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2023.zip']
        
        for url in urls:
            super().download_file_from_url(url)
            super().unzip_download()
            super().slice_data()
            
            
    # Get data from the file and return a Pandas Dataframe
    def get_data(self, file_path: str) -> pd.DataFrame:
        
        enc = 'ISO-8859-1'
        data_temp_path = super().get_data_temp_path()
        file_path = os.path.join(data_temp_path, file_path)

        # Open the file and convert to Pandas Dataframe
        data_frame = pd.read_csv(file_path, encoding=enc, sep=';', header=0, low_memory=False)
        city_name = str(data_frame['ds_municipio'].iloc[0])
        city_code = int(data_frame['codigo_municipio_ibge'].iloc[0])
        
        return data_frame, city_name, city_code
            
            


def run_multiprocessing(files, extractor, config):
            
    # Variables for multiprocessing
    cores = mp.cpu_count()
    core_multiplier = 1
    log.debug(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    num_files = len(files)
    
    progress_bar = tqdm(total=num_files, position=0)

    while completed < num_files:
        
        while running <= (cores * core_multiplier) and len(files) > 0:
            file = files.pop(0)
            p = Process(target=run_city, args=(file, extractor, config))
            processes.append(p)
            p.start()
            running += 1
            
        for process in processes:
            if not process.is_alive():
                completed += 1
                running -= 1
                processes.remove(process)
                progress_bar.update(1)
                
        time.sleep(5)


    log.info(f'Finished all files!')
    progress_bar.close()
    
    
    
def run_city(file, extractor, config):
    
    log.info(f'----- > Opening file {file}...')
    
    # Get data from Extractor
    data_tce, city_name, city_code = extractor.get_data(file)
    city = City(name=city_name, code=city_code)
    city.etl(data=data_tce, config_columns=config)
    
    log.info(f'----- > Finished file {file}...')






def run():
    
    extractor = Extractor_tce()
    #extractor.download()
    
    cities_files = []
    for file in os.listdir(extractor.get_data_temp_path(nivel=2)):
        if file.endswith('.csv'):
            cities_files.append(file)
            
    
    
    # Configura as tabelas obrigatórias no banco de dados
    # A chave primária é a combinação das colunas 'id_despesa_detalhe' e 'cd_municipio'
    # São obrigatórias as primeiras colunas, até 'cd_municipio'
    # Esquema: { "NOME_DA_COLUNA_BANCO_DADOS": "NOME_DA_COLUNA_ARQUIVO_ORIGINAL" }

    config = {
        "mes": "mes_referencia",
        "mes_extenso": "mes_ref_extenso",
        "ano": "ano_exercicio",
        "id_despesa_detalhe": "id_despesa_detalhe",
        "nr_empenho": "nr_empenho",
        "dt_emissao_despesa": "dt_emissao_despesa",
        "valor_despesa": "vl_despesa",
        "historico_despesa": "historico_despesa",
        "cd_municipio": "codigo_municipio_ibge",
        "cd_programa": "cd_programa",
        "ds_programa": "ds_programa",
        "cd_acao": "cd_acao",
        "ds_acao": "ds_acao",
        "ds_orgao": "ds_orgao",
        "tp_despesa": "tp_despesa",
        "tp_identificador_despesa": "tp_identificador_despesa",
        "nr_identificador_despesa": "nr_identificador_despesa",
        "ds_despesa": "ds_despesa",
        "ds_funcao_governo": "ds_funcao_governo",
        "ds_subfuncao_governo": "ds_subfuncao_governo",
        "ds_fonte_recurso": "ds_fonte_recurso",
        "ds_cd_aplicacao_fixo": "ds_cd_aplicacao_fixo",
        "ds_modalidade_lic": "ds_modalidade_lic",
        "ds_elemento": "ds_elemento"
    }
    
    # Filter cities
    cities_files = cities_files[:3]
    
    run_multiprocessing(cities_files, extractor, config)