import numpy as np
from matplotlib import pyplot 
import pint
# from . import lalala.py 
import sys, os
#from pysica_classes import *
import pysica_classes as psc
import pysica_plots as psp
import datetime
import pandas as pd


class Pysica(object):
    un = None
    dict_connections = {}
    def __init__(self, save_file = ''):
        self.un = pint.UnitRegistry() # não esquecer de habilitar o pyplot
        self.save_file = save_file
        # inicializar dataset padrão list_datasets. TODO: Carregar dos salvos  
        #self.dict_datasets = {}
        self.datasets=[]
        self.using_dataset = None
        #self.dataset_pointer = None
        #dataset_blank = psc.Dataset('blank', titulo='Dataset inicial, só pra não ficar em branco')
        #self.dict_datasets.update({'blank':dataset_blank})
        # inicializa lista de tags 
        #self.dict_tags = {}
        #self.dict_tags.update({'blank': Tag('blank', titulo='Tag em branco para iniciar tags')})
        #self.dict_curvas = {}
       
    def create_dataset(self, name = "Teste dataset", list_tags =[], **kwargs):
        """
        Parameters
        ----------
        tags : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        #insere na lista de datasets
        #print("?")
        dataset = psc.Dataset(name, list_tags)
        self.datasets.append(dataset)
        self.dataset_i = len(self.datasets) - 1
        return dataset

    def export_dataset(self, dataset, filename='pysca teste.xlsx', mode='excel'):
        data_var = dataset.data_var
        data_par = dataset.data_par
        schema = dataset.schema
        if mode =='excel':
            with pd.ExcelWriter(filename) as writer:
                data_par.to_excel(writer, filename, sheet_name="Parametros")    
                data_var.to_excel(writer, filename, sheet_name="Variaveis")
                schema.to_excel(writer, filename, sheet_name="Tags")
        
        
    # DEPRECATED    
    def load_dataset_sica(self, caminho, dataset = None, **kwargs): #insere um arquivo txt do SICA no dataset
        if(not dataset):
            titulo = kwargs['titulo'] if kwargs['titulo'] else 'Teste Pandas to SICA'
            dataset_obj = psc.Dataset('SICATESTE', titulo = 'Teste Pandas to SICA')
        return dataset_obj
    
    # DEPRECATED
    def create_dataset_vali(self, list_tags,  start, end, **kwargs): #carrega dados do Vali no dataset
        """
        teste doc
        """
        dataset_id = "TESTE_VALIDB"
        dataset = psc.Dataset(dataset_id, titulo = kwargs['titulo'])
        '''
        if type(dataset)==str: #cast para Dataset ao criar o objeto
            dataset = Dataset(dataset)
        '''
        dataset.load_vali_mea(list_tags, start, end)
        return dataset
    
    def plot(self, dataset, analise="run"):
        if analise == 'run': 
            psp.plot_run(dataset)
        elif analise == 'runs':
            psp.plot_runs(dataset)
        elif analise == 'qualitycw':
            psp.plot_qualitycw(dataset)
        elif analise == 'tr':
            psp.plot_tr(dataset)
        '''
        dict_actions = {
            'runs': psp.plot_runs(dataset),
            'run': psp.plot_run(dataset),
            'qualitycw': psp.plot_qualitycw(dataset),
            }
        
        dict_actions[analise]
        '''
    
    def use_dataset(self, dataset_id):
        self.current_dataset = dataset_id
        
    def plot_curva(self, curva ):
        pass
    
    def save(self, save_file = ''):
        if save_file: self.save_file = save_file
        # TODO: json_dumps de todos os objetos 
        
    def load(self, load_file):
        self.save_file  = load_file
        # TODO: abrir o arquivo e carregar os dados