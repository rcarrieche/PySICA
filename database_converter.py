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
    dados_tag_mea, colunas_tag_mea = vali_loader.get_sica1sql_tags()
    print(colunas_tag_mea)
    print(dados_tag_mea)
    origin = 'SICA1_SQL'
    for dado in dados_tag_mea:
        tag = odm.Tag(name=dado[0], description=dado[1], ue=dado[2])
        tag.origin = odm.DataOrigin.objects(name__contains=origin).first()
        tag.save()

def import_vali_dvr():
    vali_loader = ld.ValiLoader()
    mongo_loader = ld.MongoLoader(database = 'Teste') 
    
    # import tags
    dados_tag_vali, colunas_tag_vali = vali_loader.get_angra1dvr_tags()
    print(colunas_tag_vali)
    print(dados_tag_vali)
    origin = 'ANGRA1_DVR'
    for dado in dados_tag_vali:
        tag = odm.Tag(name=dado[1], description=dado[2], ue=dado[4])
        tag.origin = odm.DataOrigin.objects(name__contains=origin).first()
        tag.save()
        
    # import physical units
    
    
def import_sica():
    pass

def import_uprate():
    pass

drop_database()
populate_origin()
test_origin()
import_vali_mea()
import_vali_dvr()