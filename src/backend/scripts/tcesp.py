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
level_bar_counter = 1


"""
    Esta classe é responsável por implementar o Extractor para o TCE-SP
    Os métodos 'download', 'get_last_update' e 'get_data' são de implementação obrigatória!
    
    Devido a dificuldades em fazer a extração da data de atualização direto do site do TCE-SP, 
    o método 'get_last_update' não está implementado corretamente e será
    considerada a data de atualização do arquivo como a data de atualização do banco de dados.    
"""
class Extractor_tce(Extractor):
    
    def __init__(self):
        super().__init__(unzip=True, split_format='csv')
    
    
    def get_last_update(self):
        self.last_update = datetime.datetime.now()
        

    def download(self):
        
        urls = ['https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2023.zip']
        
        for url in urls:
            super().download_file_from_url(url)
            super().unzip_download()
            super().slice_data()
        
        self.get_last_update()

            
    # Get data from the file and return a Pandas Dataframe
    def get_data(self, file_path: str) -> pd.DataFrame:
        
        enc = 'ISO-8859-1'
        data_temp_path = super().get_data_temp_path()
        file_path = os.path.join(data_temp_path, file_path)

        # Open the file and convert to Pandas Dataframe
        data_frame = pd.read_csv(file_path, encoding=enc, sep=';', header=0, low_memory=False)

        # !! Necessita generalizar para outros arquivos através do parâmetro 'config' !!
        city_name = str(data_frame['ds_municipio'].iloc[0])
        city_code = int(data_frame['codigo_municipio_ibge'].iloc[0])
        
        return data_frame, city_name, city_code
            




# Este método é responsável pelo processamento
# de todas as cidades em paralelo

# O parâmetro CORE_MULTIPLIER é usado para forçar o uso de 100% da CPU
# pois em testes realizados, se o número de processos for igual ao número de cores,
# o uso da CPU fica relativamente baixo, o que atrasa o processamento como um todo.

def run_multiprocessing(files, extractor, config):
            
    global level_bar_counter

    # Variables for multiprocessing
    cores = mp.cpu_count()
    CORE_MULTIPLIER = 1.5
    log.debug(f'Running in {cores} cores...')
    processes = []
    running = 0
    completed = 0
    num_files = len(files)
    
    progress_bar = tqdm(total=num_files, position=0)

    while completed < num_files:
        
        while running <= (cores * CORE_MULTIPLIER) and len(files) > 0:
            file = files.pop(0)

            # Executa o método 'run_city' em um processo separado, passando o arquivo da cidade
            p = Process(target=run_city, args=(file, extractor, config, level_bar_counter))

            processes.append(p)
            level_bar_counter += 1
            p.start()
            running += 1
        
        # Organiza a lista de processos, removendo os que já terminaram
        for process in processes:
            if not process.is_alive():
                completed += 1
                running -= 1
                level_bar_counter -= 1
                processes.remove(process)
                progress_bar.update(1)
                
        time.sleep(5)


    log.info(f'Finished all files!')
    progress_bar.close()
    


# Esse método cria uma instância da classe City e executa o método 'etl'

def run_city(file, extractor, config, level_bar):
    
    log.info(f'----- > Opening file {file}...')
    
    # Obtém os dados do 'Extractor'
    # A variável 'data_tce' é um Pandas Dataframe

    data_tce, city_name, city_code = extractor.get_data(file)

    city = City(name=city_name, code=city_code, origin='tcesp')
    
    # Nível da barra de progresso
    city.level_bar = level_bar
    
    # Executa os processos de Extract, Transform e Load
    city.etl(data=data_tce, config_columns=config)
    
    log.info(f'----- > Finished file {file}...')







"""
    Executa a extração e processamento de dados do TCE-SP.
    Esta função faz o download dos dados do TCE-SP, processa-os e armazena-os em um banco de dados.
    A função utiliza a classe Extractor_tce para fazer o download dos dados e
    a configuração das tabelas obrigatórias no banco de dados é feita através do dicionário 'config'.
"""
def run():
    
    extractor = Extractor_tce()
    extractor.download()
    extractor.filter_cities(pop=5)
    
    cities_files = []
    for file in os.listdir(extractor.get_data_temp_path(nivel=2)):
        if file.endswith('.csv'):
            cities_files.append(file)
            
    
    """
        Configura as tabelas obrigatórias no banco de dados
        A chave primária é a combinação das colunas 'id_despesa_detalhe' e 'cd_municipio'
        São obrigatórias as primeiras colunas, até 'cd_municipio'
        
        Esquema: { "NOME_DA_COLUNA_BANCO_DADOS": "NOME_DA_COLUNA_ARQUIVO_ORIGINAL" }
    """

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
    
    run_multiprocessing(cities_files, extractor, config)