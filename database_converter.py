# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 11:28:05 2021

@author: nato
"""
import loaders as ld
import pysica_classes as pysc
import numpy as np
from matplotlib import pyplot 
import pint
# from . import lalala.py 
import sys, os
import datetime
import odm
import pymongo as pm
import pandas as pd

MONGO_DATABASE = 'Teste4'

def tagficator(tagname):
    return tagname.strip('[]').replace('-.', '_').upper()

def drop_database():
    print("Descartando banco anterior")
    mongo_loader = ld.MongoLoader(database = MONGO_DATABASE)
    mongo_loader.db.drop_database(MONGO_DATABASE)

def populate_origin():
    print("inserindo origens iniciais")
    mongo_loader = ld.MongoConnection(database = MONGO_DATABASE)
    initial_origins = ['SICA1_SQL', 'ANGRA1_DVR', 'SICA_FILE', 'UPRATE']
    for origin in initial_origins:
        data_origin = odm.DataOrigin(name=origin, description=origin)
        data_origin.save()
        
        
def test_origin():
    data_origin = odm.DataOrigin.objects()
    print(data_origin)
    
def import_vali_mea():
    vali_loader = ld.ValiLoader()
    mongo_loader = ld.MongoLoader(database = MONGO_DATABASE) 
    
    
    # definindo origem
    origin_name = 'SICA1_SQL'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_sica1sql_ue()
    for dado in dados_ue:
        ue = odm.UE(name=dado[0], data_origin = origin)
        ue.save()
    
    # insere tags
    dados_tag_mea, colunas_tag_mea = vali_loader.get_sica1sql_tags()
    for dado in dados_tag_mea:
        tag = odm.Tag(name=dado[0], description=dado[1], ue=dado[2])
        tag.data_origin = origin
        ue = odm.UE.objects(name = dado[2], data_origin = origin).first()
        tag.ue = ue
        tag.save()
    
    
    # definindo dataset
    dataset = odm.Dataset(name = 'SICA1_SQL DATASET TESTE', data_origin = origin).save()
    
    # importando dados do SICA1_SQL
    dados_mea, colunas_mea = vali_loader.get_sica1sql_values()
    for dado in dados_mea:
        tag = odm.Tag.objects(name=dado[0], data_origin = origin).first()
        tagval = odm.TagVal(tag=tag, val=dado[2], date=dado[1], dataset = dataset)
        tagval.values = {}
        for val, coluna in zip(dado, colunas_mea):
            #taguificar coluna
            #TODO: regex
            col_fmt = tagficator(coluna)
            tagval.values.update({col_fmt:val})
            #setattr(tagval, coluna.upper())
        tagval.save()


def import_vali_dvr():
    vali_loader = ld.ValiLoader()
    mongo_loader = ld.MongoLoader(database = MONGO_DATABASE) 
    
    # definindo origem
    origin_name = 'ANGRA1_DVR'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_angra1dvr_ue()
    for dado in dados_ue:
        ue = odm.UE(name=dado[1], original_id = dado[0], data_origin = origin)
        ue.save()
        
    # import tags
    dados_tag_vali, colunas_tag_vali = vali_loader.get_angra1dvr_tags()
    for dado in dados_tag_vali:
        tag = odm.Tag(name=dado[1], description=dado[2])
        tag.data_origin = origin
        ue = odm.UE.objects(name = dado[4], data_origin = origin).first()
        #print("Tag: {}    Origem: {}        UE Original: {}     UE buscado: {}".format(tag.name, tag.data_origin.name, dado[4], ue.name))
        tag.ue = ue
        tag.save()
        
    
    
    # definindo dataset
    dataset = odm.Dataset(name = 'ANGRA1_DVR DATASET TESTE', data_origin = origin).save()
    
    # import runs
    dados_run, colunas_run = vali_loader.get_runs()
    for dado in dados_run:
        run = odm.Run(
            date = dado[colunas_run.index('Date')]
            ,original_id = dado[colunas_run.index('Run')]
            ,dataset = dataset
        )
        run.values = {}
        for val, coluna in zip(dado, colunas_run):
            col_fmt = tagficator(coluna)
            run.values.update({col_fmt:val})
        run.save()    
    
    # importando dados do ANGRA1_DVR
    dados_mea, colunas_mea = vali_loader.get_angra1dvr_values()
    for dado in dados_mea:
        tag = odm.Tag.objects(name=dado[0], data_origin = origin).first()
        tagval = odm.TagVal(tag=tag, val=dado[2], date=dado[1], run = odm.Run.objects(original_id=dado[colunas_mea.index('Run')]))
        tagval.values = {}
        for val, coluna in zip(dado, colunas_mea):
            #taguificar coluna
            #TODO: regex
            col_fmt = tagficator(coluna)
            tagval.values.update({col_fmt:val})
            #setattr(tagval, coluna.upper())
        tagval.save()
        
def update_tag_same_as():
    # TODO: não repetir tags
    mongo_loader = ld.MongoLoader(database = MONGO_DATABASE)
    data_origins = odm.DataOrigin.objects()
    for origin in data_origins:
        qs = odm.Tag.objects(data_origin__in=odm.DataOrigin.objects(name=origin.name))
        print("Origem: "+origin.name)
        for tag in qs:
            print("Atualizando tag "+tag.name)
            tags_outros = odm.Tag.objects(name=tag.name, data_origin__ne=odm.DataOrigin.objects(name=origin.name).first())
            for ts in tags_outros:
                print("inserindo tag {} de {} em {}".format(ts.name, ts.data_origin.name, tag.name))
                #tag.tag_same_as.append(ts)
                tag.update(push__tag_same_as=ts)
                # ts.tag_same_as.append(tag)
            
def normalizar_ue():
    loader = ld.MongoLoader(database = MONGO_DATABASE)
    mongo_cliente = pm.MongoClient()
    db = mongo_cliente[MONGO_DATABASE]
    print(db.u_e)
    
    for x in db.u_e.find():
        #print(x)
        pass
    for x in db.tag.find({'name': {'$in':['PI1980A', 'TE6540']}}): 
        try: 
            print("{}:   {} from {}".format(x['name'], x['ue'], x['data_origin']))
        except Exception as e:
            print(x)
            print(e)
            
            
def update_tag_components():
    data_origin_name = 'ANGRA1_DVR'
    
    
    
def import_sica_tags():
    # definindo origem
    mongo_loader = ld.MongoLoader(database = MONGO_DATABASE)
    origin_name = 'SICA_FILE'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    loader = ld.SicaLoader()
    filepath = 'C:\\Users\\nato\\Pysica\\data\\SICA\\Analogicas.txt'
    df_tags = loader.read_sica_tags(filepath)
    #print(df_tags['Referencia'])
    #dir(df_tags)
    for i, linha in df_tags.iterrows():
        # TODO: busca ue e cria nova se não existe
        #print(linha)
        tag = odm.Tag(name = linha['Referencia'], description=linha['Descricao'], data_origin = origin)
        tag.alt_names = [linha['Codigo_Instrumento']]
        ue = odm.UE.objects(name = linha['Unidade_Engenharia'], data_origin = origin).first()
        #ue = odm.UE.objects(name = linha['Unidade_Engenharia'])
        if not ue:
            ue = odm.UE(name= linha['Unidade_Engenharia'], data_origin = origin).save()
        tag.ue = ue
        tag.save()

def import_sica_values():
    loader = ld.SicaLoader()
    dirpath = 'C:\\Users\\nato\\Pysica\\data\\SICA\\dat'
    loader.read_sica_batch(dirpath)

def import_uprate():
    pass

def bound_tags():
    pass

def import_pepse():
    pass

def import_csv():
    pass

def import_LV():
    pass

def import_LSR():
    pass

drop_database()
"""

populate_origin()
test_origin()
import_vali_mea()

import_vali_dvr()

import_sica_tags()
update_tag_same_as()

"""
import_sica_values()

#normalizar_ue()

"""
import winsound
duration = 2000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
"""

