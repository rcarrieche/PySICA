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

def tagficator(tagname):
    return tagname.strip('[]').replace('-.', '_').upper()

def drop_database():
    mongo_loader = ld.MongoLoader(database = 'Teste')
    mongo_loader.db.drop_database('Teste')

def populate_origin():
    mongo_loader = ld.MongoConnection(database = 'Teste')
    initial_origins = ['SICA1_SQL', 'ANGRA1_DVR', 'SICA_FILE', 'UPRATE']
    for origin in initial_origins:
        data_origin = odm.DataOrigin(name=origin, description=origin)
        print(data_origin)
        data_origin.save()
        
        
def test_origin():
    data_origin = odm.DataOrigin.objects()
    print(data_origin)
    
def import_vali_mea():
    vali_loader = ld.ValiLoader()
    mongo_loader = ld.MongoLoader(database = 'Teste') 
    
    
    # definindo origem
    origin_name = 'SICA1_SQL'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_sica1sql_ue()
    for dado in dados_ue:
        ue = odm.UE(name=dado[0], original_id = dado[1], data_origin = origin)
    
    # insere tags
    dados_tag_mea, colunas_tag_mea = vali_loader.get_sica1sql_tags()
    for dado in dados_tag_mea:
        tag = odm.Tag(name=dado[0], description=dado[1], ue=dado[2])
        tag.data_origin = origin
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
    mongo_loader = ld.MongoLoader(database = 'Teste') 
    
    # definindo origem
    origin_name = 'ANGRA1_DVR'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_angra1dvr_ue()
    for dado in dados_ue:
        ue = odm.UE(name=dado[0], original_id = dado[1], data_origin = origin)
        ue.save()
        
    # import tags
    dados_tag_vali, colunas_tag_vali = vali_loader.get_angra1dvr_tags()
    for dado in dados_tag_vali:
        tag = odm.Tag(name=dado[1], description=dado[2], ue=dado[4])
        tag.data_origin = origin
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
    
     # definindo dataset
    dataset = odm.Dataset(name = 'ANGRA1_DVR DATASET TESTE', data_origin = origin).save()
    
    # importando dados do ANGRA1_DVR
    dados_mea, colunas_mea = vali_loader.get_angra1dvr_values()
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
    
def update_tag_same_as():
    mongo_loader = ld.MongoLoader(database = 'Teste')
    qs_vali = odm.Tag.objects.filter(data_origin__in=odm.DataOrigin.objects(name='ANGRA1_DVR'))
    print(qs_vali)
    for tag in qs_vali:
        #print(tag)
        tags_outros = odm.Tag.objects(name=tag.name, data_origin__name__ne='ANGRA1_DVR')
        for ts in tags_outros:
            tag.tag_same_as.append(ts)
            ts.tag_same_as.append(tag)
            
            
def update_tag_components():
    pass
    
def import_sica_tags():
    pass

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
populate_origin()
test_origin()
import_vali_mea()
import_vali_dvr()

update_tag_same_as()