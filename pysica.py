import numpy as np
from matplotlib import pyplot 
import pint
# from . import lalala.py 
import sys, os
from pysica_classes import *
import datetime

class Pysica(object):
    un = None
    dict_connections = {}
    def __init__(self, save_file = ''):
        self.un = pint.UnitRegistry() # não esquecer de habilitar o pyplot
        self.save_file = save_file
        # inicializar dataset padrão list_datasets. TODO: Carregar dos salvos  
        self.dict_datasets = {}
        dataset_blank = Dataset('blank', titulo='Dataset inicial, só pra não ficar em branco')
        self.dict_datasets.update({'blank':dataset_blank})
        # inicializa lista de tags 
        self.dict_tags = {}
        self.dict_tags.update({'blank': Tag('blank', titulo='Tag em branco para iniciar tags')})
        self.dict_curvas = {}
       
    def gera_dataset(self, datetime_inicio, datetime_fim):
        #insere na lista de datasets
        pass
    def load_dataset_sica(self, caminho, dataset = None, **kwargs): #insere um arquivo txt do SICA no dataset
        if(not dataset):
            titulo = kwargs['titulo'] if kwargs['titulo'] else 'Teste Pandas to SICA'
            dataset_obj = Dataset('SICATESTE', titulo = 'Teste Pandas to SICA')
        return dataset_obj
    
    
    def create_dataset_vali(self, list_tags,  start, end, **kwargs): #carrega dados do Vali no dataset
        """
        teste doc
        """
        dataset_id = "TESTE_VALIDB"
        dataset = Dataset(dataset_id, titulo = kwargs['titulo'])
        '''
        if type(dataset)==str: #cast para Dataset ao criar o objeto
            dataset = Dataset(dataset)
        '''
        dataset.load_vali_mea(list_tags, start, end)
        return dataset
    
    def plot_dataset(self, lista_tags, lista_unidades): 
        pass
    
    def use_dataset(self, dataset_id):
        this.current_dataset = dataset_id
        
    def plot_curva(self, curva ):
        pass
    
    def save(save_file = ''):
        if save_file: self.save_file = save_file
        # TODO: json_dumps de todos os objetos
        
    def load(load_file):
        self.save_file  = load_file
        # TODO: abrir o arquivo e carregar os dados