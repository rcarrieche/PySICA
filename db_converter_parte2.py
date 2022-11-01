# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:27:35 2022

@author: nato
"""
from constantes import *
from pymongo import MongoClient
import odm
from mongoengine import connect, disconnect
import pandas as pd
import os
from pprint import pprint
import sys
import datetime
import re
import time
import loaders as ld


print("a")
disconnect()
client = MongoClient()
db = client.get_database(MONGO_DATABASE)
connect(db=MONGO_DATABASE, host='localhost')

def db_init(f):
    def wrapper():
        tempo_inicial = time.time()
        f()
        tempo_final = time.time()
        t = tempo_final - tempo_inicial
        print("\nFunção: {0}\nTempo de execução: {1}".format(f.__name__, t))
    return wrapper

def tagficator(tagname):
    string = re.sub(r'[\]\[]', "", tagname.strip())
    string = re.sub(r'[\-\./ ]', "_", string)
    return string.upper()


@db_init        
def import_uprate():
    #TODO: preparar os dados na planilha
    #TODO: não é melhor importar direto do PEPSE?
    with pd.ExcelWriter(EXCEL_UPRATE) as w:
        
        pass

@db_init
def import_LV():
    pass

@db_init
def import_dvr_restantes():
    # definindo origem
    origin_name = 'ANGRA1_DVR'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    tags = odm.Tag.objects(data_origin=data_origin)
    vali_loader = ld.ValiLoader()
    list_tags_restantes = []
    for tag in tags:
        tagvars = odm.TagVar.objects(tag = tag) 
        mapa = {}
        values_count = 0
        for var in tagvars:
            values_count = values_count + odm.Values.objects(tag_var = var).count()
        if values_count > 0:
            print("Temos {} valores registrados para o tag {}".format(values_count, tag['name']))
            print(tag['id'])
        else:
            print("Tag {} sem valores!".format(tag['name']))
            list_tags_restantes.append(tag["id"])
    tags_restantes = odm.Tag.objects(id__in=list_tags_restantes)
    tagnames = tags_restantes.values_list('original_name')
    #print(tagnames)
    #sys.exit()
    """
    dados_mea, colunas_mea = vali_loader.get_angra1dvr_values(None, tagnames)
    df = pd.DataFrame(dados_mea, columns=colunas_mea)
    for tag in tags_restantes:
        print("analisando tag "+tag['name'])
        tagvars = odm.TagVar.objects(tag=tag)
        list_values = []
        for tagvar in tagvars:
            if tagvar['original_name'] not in df.columns: continue
            #list_values = []
            var_name = tagvar['original_name']
            categorical = tagvar['categorical']
            print("Processando var {0} do tag {1}".format(var_name, tag['name']))
            def insert_row(row):
                print("val")
                #run = odm.Run.objects(original_id=row['Run']).first()
                #list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar, run = run))
                if(categorical):
                    list_values.append(odm.Values(valcat=row[var_name], date=row['Date'], tag_var = tagvar))
                else:
                    list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar))
                print(list_values)
            
            a = df[['Name','Date', var_name, 'Run']]
            print(a.head())
            filtro = df['Name'] == tag['original_name']
            print(a[filtro].head())
            a[filtro].apply(insert_row, axis=1)
            
        if list_values:
            odm.Values.objects.insert(list_values)             
        else:
            print("list_values vazio!!!")
            
        
    """
    
    for tag in tags_restantes:
        print("importando "+tag['name'])
        print(tag['original_name'])
        dados_mea, colunas_mea = vali_loader.get_angra1dvr_values(tag['original_name'])
        df = pd.DataFrame(dados_mea, columns=colunas_mea)
        tagvars = odm.TagVar.objects(tag=tag)
        list_values = []
        for tagvar in tagvars:
            if tagvar['original_name'] not in df.columns: continue
            #list_values = []
            var_name = tagvar['original_name']
            categorical = tagvar['categorical']
            def insert_row(row):
                #print("função insert_row")
                #run = odm.Run.objects(original_id=row['Run']).first()
                #list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar, run = run))
                list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar))
            a = df[['Name','Date', var_name, 'Run']]
            a.apply(insert_row, axis=1)
            
        if list_values:
            odm.Values.objects.insert(list_values)               
        else:
            print("list_values vazio!!!")
            #print(df.head())
    print(tags_restantes)



def liga_nomes():
    data_origins = odm.DataOrigin.objects()
    tags = odm.Tag.objects() 
    print(data_origins.values_list('name'))
    for tag in tags:
        similar_tags = odm.Tag.objects(name=tag['name'], id__ne=tag['id']) # todos os tags de mesmo nome ou mesmo nome original, excluindo o tag que estamos buscando 
        if similar_tags:
            
            print(similar_tags.values_list('name'), similar_tags.values_list('data_origin'))
            related = tag["tag_related"]
            print(related)
            [related.append(st) for st in similar_tags]
            tag["tag_related"] = related
            print(tag["tag_related"])
            
            tag.save()
            print("tag "+tag['name']+"  inseridos: "+str(len(similar_tags)))
        else:
            print(""+tag['name']+" sem similar por nome!")
        
        
def create_sica_instruments():
    
    pass

def liga_malhas():
    pass



# Finalizando ANGRA1_DVR import
#import_dvr_restantes()

# cria tags dos equipamentos do Vali

#-- UPRATE
#import_uprate()

#-- KIT TERMICO

#-- PEPSE
# import_pepse_tags()
# import_pepse_values()


#-- EMSO

#-- LISTAGEM DE VÁLVULAS
#import_LV()

#-- SET POINTS E RANGES

#-- PSI

#-- PASR

# RETIFICADORES E CORREÇÕES
liga_nomes()
create_sica_instruments()
