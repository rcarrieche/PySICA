# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:30:29 2022

@author: nato
"""
import loaders as ld
from constantes import *
from pymongo import MongoClient
import odm
from mongoengine import connect
import pandas as pd
import os
from pprint import pprint
import sys
import datetime
import re
import time

"""
client = MongoClient()
db = client.get_database(MONGO_DATABASE)
connect(db=MONGO_DATABASE, host='localhost')
vali_loader = ld.ValiLoader()
"""
client = MongoClient()
db = client.get_database(MONGO_DATABASE)
connect(db=MONGO_DATABASE, host='localhost')
#vali_loader = ld.ValiLoader()

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
def drop_database():
    print("\n\n*** Descartando banco anterior...")
    client.drop_database(MONGO_DATABASE)

@db_init
def popular_origens():
    print("\n\n*** Populando origens...")
    coll_origin = db.get_collection('data_origin')
    origens_ids = coll_origin.insert_many(ORIGENS)
    return origens_ids

@db_init
def import_dvr_tags():
    print("\n\n*** Importando tags...")
    vali_loader = ld.ValiLoader()
    origin_name = 'ANGRA1_DVR'
    print(origin_name)
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    #origin = db.get_collection('data_origin').find_one({'name':origin_name})
    #origin_id = origin['_id']
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_angra1dvr_ue()
    for dado in dados_ue:
        ue = odm.MeaUnit(name=dado[1], original_id = dado[0], data_origin = origin)
        #um = {'name':dado[1]}
        ue.save()
    
    # import tags
    dados_tag_vali, colunas_tag_vali = vali_loader.get_angra1dvr_tags()
    tags = []
    for dado in dados_tag_vali:
        tag = odm.Tag(name=tagficator(dado[1]), description=dado[2], original_name=dado[1])
        tag.data_origin = origin
        ue = odm.MeaUnit.objects(name = dado[4], data_origin = origin).first()
        #print("Tag: {}    Origem: {}        UE Original: {}     UE buscado: {}".format(tag.name, tag.data_origin.name, dado[4], ue.name))
        tag.mea_unit = ue
        tags.append(tag)
    odm.Tag.objects.insert(tags)

@db_init
def create_dvr_vars():
    print("\n\n*** Criando varíaveis ...")
    origin_name = 'ANGRA1_DVR'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    # create master vars
    df_tagvar = pd.DataFrame(TAGVAR_DVR)
    vars_list = df_tagvar.to_dict('records')
    #mea_unit = odm.MeaUnit.objects(name=, values)
    for var in vars_list:
        tagvar = odm.TagVar(name=tagficator(var['name']), original_name = var['name'], unit=var['mea_unit'], description="Variável pai para nomear variável do Vali: "+var['name'], data_origin = data_origin)
        tagvar.save()
    
    # get tags
    tags = odm.Tag.objects(data_origin=data_origin)
    master_tagvar_vali = odm.TagVar.objects(data_origin = data_origin)
    for tag in tags:
        for master_var in master_tagvar_vali:
            is_categorical = False
            ue = None
            if master_var['mea_unit'] == 'var':
                ue = odm.MeaUnit.objects(_id=tag['mea_unit']) #entra a ue do tag
                unit_name = ue['name']
            elif master_var['mea_unit'] == 'Int':
                is_categorical = True
                unit_name = ''
            else:
                unit_name = master_var['mea_unit']
            description = '('+master_var['name']+') '+tag['name']+' - '+tag['description']+' - '+master_var['description']
            tagvar = odm.TagVar(name=master_var['name'], original_name=master_var['original_name'], description = description, tag = tag, alias=[tag['name']], unit=unit_name, mea_unit = ue, data_origin=data_origin, categorical = is_categorical)
            tagvar.save()

@db_init
def import_dvr_runs():
    print("\n\n*** Importando runs...")
    vali_loader = ld.ValiLoader()
    # import runs
    dados_run, colunas_run = vali_loader.get_runs()
    runs=[]
    for dado in dados_run:
        run = odm.Run(
            date = dado[colunas_run.index('Date')]
            ,original_id = dado[colunas_run.index('Run')]
        )
        run.values = {}
        for val, coluna in zip(dado, colunas_run):
            col_fmt = tagficator(coluna)
            run.values.update({col_fmt:val})
        #run.save()
        runs.append(run)
    odm.Run.objects.insert(runs)

@db_init
def import_sicasql_tags():
    print("\n\n*** Importando tags SICA1_SQL ...")
    vali_loader = ld.ValiLoader()
    
    # definindo origem
    origin_name = 'SICA1_SQL'
    print(origin_name)
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    
    # import physical units
    dados_ue, col_ue = vali_loader.get_sica1sql_ue()
    for dado in dados_ue:
        ue = odm.MeaUnit(name=dado[0], data_origin = origin)
        ue.save()
    
    # insere tags
    dados_tag_mea, colunas_tag_mea = vali_loader.get_sica1sql_tags()
    for dado in dados_tag_mea:
        tag = odm.Tag(name=tagficator(dado[0]), original_name = dado[0], description=dado[1], mea_unit=dado[2])
        tag.data_origin = origin
        ue = odm.MeaUnit.objects(name = dado[2], data_origin = origin).first()
        tag.mea_unit = ue
        tag.save()

@db_init        
def create_sicasql_vars():
    print("\n\n*** Criando varíaveis SICA1_SQL ...")
    origin_name = 'SICA1_SQL'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    # create master vars
    df_tagvar = pd.DataFrame(TAGVAR_SICA1_SQL)
    vars_list = df_tagvar.to_dict('records')
    #mea_unit = odm.MeaUnit.objects(name=, values)
    for var in vars_list:
        tagvar = odm.TagVar(name=tagficator(var['name']), original_name = var['name'], unit=var['mea_unit'], description="Variável pai para nomear variável do banco SICA1_SQL: "+var['name'], data_origin = data_origin)
        tagvar.save()
    
    # get tags
    tags = odm.Tag.objects(data_origin=data_origin)
    master_tagvar_vali = odm.TagVar.objects(data_origin = data_origin)
    for tag in tags:
        for master_var in master_tagvar_vali:
            is_categorical = False
            ue = None
            if master_var['mea_unit'] == 'var':
                ue = odm.MeaUnit.objects(_id=tag['mea_unit']) #entra a ue do tag
                unit_name = ue['name']
            elif master_var['mea_unit'] == 'Int':
                is_categorical = True
                unit_name = ''
            else:
                unit_name = master_var['mea_unit']
            description = ''+tag['name']+' - '+tag['description']+' - '+master_var['description']+' ('+unit_name+')'
            tagvar = odm.TagVar(name=master_var['name'], original_name=master_var['original_name'], description = description, tag = tag, alias=[tag['name']], unit=unit_name, mea_unit = ue, data_origin=data_origin, categorical = is_categorical, parent_var=master_var)
            tagvar.save()

@db_init        
def import_sica_tags():
    print("\n\n*** Importando tags SICA_TXT ...")
    #coll_mea_unit = db.get_collection('mea_unit')
    # definindo origem
    origin_name = 'SICA_TXT'
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    df_raw = pd.read_fwf(SICA_TAGFILE, encoding = 'ISO-8859-1')
    list_tags_sica = df_raw.to_dict('records')
    for ref in list_tags_sica:
        ue_str = ref['Unidade_Engenharia']
        ue = odm.MeaUnit.objects(name=ue_str, data_origin = origin).modify(upsert=True, set__name=ue_str, set__data_origin=origin)
        #k={'name':ue_str}
        #coll_mea_unit.update(k, kwargs)
        tag = odm.Tag(name=tagficator(ref["Referencia"]), original_name=ref["Referencia"], description=ref['Descricao'], alt_names=[ref['Codigo_Instrumento']], data=ref, mea_unit = ue, data_origin=origin) 
        tag.save()

@db_init
def create_sica_vars():
    print("\n\n*** Criando varíaveis SICA_TXT ...")
    origin_name = 'SICA_TXT'
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    # create master vars
    df_tagvar = pd.DataFrame(TAGVAR_SICA_TXT)
    vars_list = df_tagvar.to_dict('records')
    #mea_unit = odm.MeaUnit.objects(name=, values)
    for var in vars_list:
        tagvar = odm.TagVar(name=tagficator(var['name']), original_name = var['name'], unit=var['mea_unit'], description="Variável pai para nomear variável SICA: "+var['name'], data_origin = data_origin)
        tagvar.save()
    
    # get tags
    tags = odm.Tag.objects(data_origin=data_origin)
    master_tagvar_vali = odm.TagVar.objects(data_origin = data_origin)
    for tag in tags:
        for master_var in master_tagvar_vali:
            is_categorical = False
            ue = None
            if master_var['mea_unit'] == 'var':
                ue = odm.MeaUnit.objects(_id=tag['mea_unit']) #entra a ue do tag
                unit_name = ue['name']
            elif master_var['mea_unit'] == 'Int':
                is_categorical = True
                unit_name = ''
            else:
                unit_name = master_var['mea_unit']
            description = ''+tag['name']+' - '+tag['description']+' - '+master_var['description']
            tagvar = odm.TagVar(name=master_var['name'], original_name=master_var['original_name'], description = description, tag = tag, alias=[tag['name']], unit=unit_name, mea_unit = ue, data_origin=data_origin, categorical = is_categorical, parent_var=master_var)
            tagvar.save()

@db_init
def import_ovation():
    
    origin_name = 'OVATION'
    print("\n\n*** Importando de "+origin_name+"...")
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    caminhos = [OVATION_DIR]
        
    for caminho in caminhos:
        arquivos = os.listdir(caminho)
        for arquivo in arquivos:
            print(arquivo)
            #TODO: encode pro arquivo ovation. Abrir com Pandas sem precisar de tratamento externo
            df_raw = pd.read_csv(caminho+arquivo, sep='\t', encoding='UTF-16LE')
            #df_raw.dropna()
            dict_dados = df_raw.to_dict()
            chaves = dict_dados.keys()
            #chaves = df_raw.columns
            df_raw['date'] = pd.to_datetime(df_raw.iloc[:,0].str.strip(), format="%m/%d/%Y %H:%M:%S.000 %p")
            
            for chave in chaves:
                tagname = chave.split('@')[0]
                tag = odm.Tag(name=tagname, original_name=chave, data_origin=origin )
                tag.save()
                tagvar = odm.TagVar(tag=tag, name='val', original_name=chave, unit=None, mea_unit=None)
                tagvar.save()
                """
                tag = odm.Tag.objects(name=tagname, data_origin=origin).first()
                #if not tag
                if true:
                    tag = odm.Tag(name=tagname, original_name=chave, data_origin=origin )
                    tag.save()
                    tagvar = odm.TagVar(tag=tag, name='val', original_name=chave, unit=None, mea_unit=None)
                    tagvar.save()
                """
                df = df_raw.drop('Date/Time', axis=1)
                list_values = []
                try:
                    
                    df.apply(lambda row: list_values.append(odm.Values(val=row[chave], date=row['date'], tag_var=tagvar)), axis=1)
                    a = odm.Values.objects.insert(list_values)
                    #df_raw.apply(f)
                except:
                    pass
                #df_raw.apply(lambda row: list_values.append(odm.Values(val=row[chave], date=row['date'])))
                
    

@db_init
def import_simulador():
    origin_name = 'SIMULADOR_A1'
    print("\n\n*** Importando de "+origin_name+"...")
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    caminhos = [SIMULADOR_DIR]
        
    for caminho in caminhos:
        print(caminho)
        arquivos = os.listdir(caminho)
        for arquivo in arquivos:
            print(arquivo)
            if arquivo[0] == "!": continue
            df_raw = pd.read_csv(caminho+arquivo, sep='\t')
            dict_dados = df_raw.to_dict()
            chaves = list(dict_dados.keys())
            #print(chaves)
            #sys.exit(0)
            #chaves = df_raw.columns
            df_raw['date'] = pd.to_datetime(df_raw.iloc[:,0].str.strip(), format="%H:%M:%S")
            
            #print(df_raw['date'])
            tagname = chaves[3]
            tag = odm.Tag(name=tagname, original_name=tagname, data_origin=origin )
            tag.save()
            tagvar = odm.TagVar(tag=tag, name='val', original_name=tagname, unit=None, mea_unit=None)
            tagvar.save()
            list_values = []
            df_raw.apply(lambda row: list_values.append(odm.Values(val=row[tagname], date=row['date'], tag_var=tagvar)), axis=1)
            a = odm.Values.objects.insert(list_values)

@db_init
def import_simulador_ovation():
    origin_name = 'SIMULADOR_OVATION'
    print("\n\n*** Importando de "+origin_name+"...")
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    caminhos = [SIMULADOR_OVATION_DIR]
    for caminho in caminhos:
        arquivos = os.listdir(caminho)
        for arquivo in arquivos:
            print(arquivo)
            #TODO: encode pro arquivo ovation. Abrir com Pandas sem precisar de tratamento externo
            df_raw = pd.read_csv(caminho+arquivo, sep='\t', encoding='UTF-8')
            df_raw['date'] = pd.to_datetime(df_raw.iloc[:,0].str.strip(), format="%m/%d/%Y %H:%M:%S %p")
            print([coluna for coluna in df_raw.columns])
            #print(df_raw['Date/Time'])
            df_raw = df_raw.drop(df_raw.columns[0], axis=1)
            chaves = df_raw.columns
            excluidos = ['Date/Time', 'date']
            for chave in chaves:
                if chave in excluidos: continue
                tagname = tagficator(chave.split('@')[0])
                tag = odm.Tag(name=tagname, original_name=chave, data_origin=origin )
                tag.save()
                tagvar = odm.TagVar(tag=tag, name='val', original_name=chave, unit=None, mea_unit=None)
                tagvar.save()
                
                list_values = []
                
                def insert_row(row):
                    
                    list_values.append(odm.Values(val=row[chave], date=row['date'], tag_var=tagvar))
                df_raw.apply(insert_row, axis=1)
                a = odm.Values.objects.insert(list_values)
                
                #df_raw.apply(lambda row: list_values.append(odm.Values(val=row[chave], date=row['date'])))
                
@db_init
def import_sica_values():
    
    origin_name = 'SICA_TXT'
    print(origin_name)
    print("\n\n*** Importando valores de "+origin_name+"...")
    origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    #df_raw = pd.read_fwf(SICA_TAGFILE, encoding = 'ISO-8859-1')
    #pastas = ['!dados2021\\', '!stretch_out_2022\\', '!Parada e partida 2021\\', '!uprate_lote1\\', 'partida 2022\\', 'Dados SICA 2020-11-14 10s\\']
    pastas = ['partida 2022\\', 'Dados SICA 2020-11-14 10s\\']
    #pastas = ['!dados2021\\']
    caminhos = [SICA_IMPORT_DIR+pasta for pasta in pastas]
    
        
    for caminho in caminhos:
        print(caminho)
        arquivos = os.listdir(caminho)
        for arquivo in arquivos:
            print(arquivo)
            # name, description, mea_unit, date, value, status 
            colspec = [(0,7), (8, 59), (59,70),(70,90), (91,116), (116,-1)]
            df_raw = pd.read_fwf(caminho+arquivo, encoding = 'ISO-8859-1', colspecs=colspec)
            colunas_raw = df_raw.columns
            colunas_novas = ['name', 'description', 'mea_unit', 'date', 'val', 'status']
            #print(colunas_raw)
            #print(colunas_novas)
            dict_colunas = {}
            for velha, nova in zip(colunas_raw, colunas_novas):
                dict_colunas.update({velha:nova})
            df = df_raw.rename(dict_colunas, axis=1)
            #print(dict_colunas)
            #print(df[['date', 'status']].head(5))
            #print(df[['description', 'mea_unit']].head(5))
            df['date'] = pd.to_datetime(df['date'])
            names = df['name'].unique()
            for name in names:
                tag = odm.Tag.objects(name = name, data_origin = origin).first()
                valor = odm.TagVar.objects(tag = tag, name='VALOR').first()
                status = odm.TagVar.objects(tag = tag, name='STATUS').first()
                list_values = []
                filtro = df['name'] == name
                df[filtro].apply(lambda row: list_values.append(odm.Values(val=row['val'], date=row['date'], tag_var=valor)), axis=1)
                df[filtro].apply(lambda row: list_values.append(odm.Values(val=row['status'], date=row['date'], tag_var=status)), axis=1)
                odm.Values.objects.insert(list_values)

@db_init            
def import_sicasql_values():
    print("\n\n*** importando valores")
    # definindo origem
    origin_name = 'SICA1_SQL'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    # importando dados do SICA1_SQL
    vali_loader = ld.ValiLoader()
    dados_mea, colunas_mea = vali_loader.get_sica1sql_values()
    df_dados_mea = pd.DataFrame(dados_mea)
    df_dados_mea = df_dados_mea.rename(columns={0:'name', 1:'date',2:'val'})
    #print(df_dados_mea.iloc[3300:3310,[0,2]])
    #sys.exit()
    list_tagnames = df_dados_mea['name'].unique()
    tags = odm.Tag.objects(name__in=list_tagnames, data_origin=data_origin)
    
    for tag in tags:
        print("importando "+tag['name'])
        list_values = []
        tagvar = odm.TagVar.objects(tag=tag, original_name="Value_Average").first()
        filtro = df_dados_mea['name'] == tag['name'] 
        def insert_values(row):
            list_values.append(odm.Values(val=row['val'], date=row['date'], tag_var=tagvar))
        df_dados_mea[filtro].apply(insert_values, axis=1)
        a = odm.Values.objects.insert(list_values)
        #print(a)
        

@db_init    
def import_dvr_values():
    # definindo origem
    origin_name = 'ANGRA1_DVR'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    tags = odm.Tag.objects(data_origin=data_origin)
    vali_loader = ld.ValiLoader()
    for tag in tags:
        print("importando "+tag['name'])
        print(tag['original_name'])
        try: 
            dados_mea, colunas_mea = vali_loader.get_angra1dvr_values(tag['original_name'])
        except:
            print("ERRO DE EXECUÇÃO: O CURSOR SUMIU!!!!")
            vali_loader = ld.ValiLoader()
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
                #run = odm.Run.objects(original_id=row['Run']).first()
                #list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar, run = run))
                list_values.append(odm.Values(val=row[var_name], date=row['Date'], tag_var = tagvar))
            a = df[['Date', var_name, 'Run']]
            a.apply(insert_row, axis=1)
            
        if list_values:
            odm.Values.objects.insert(list_values)               
        else:
            print("list_values vazio!!!")
            #print(df.head())
                
@db_init
def import_osciloscopio():
    # definindo origem
    origin_name = 'OSCILOSCOPIO'
    print(origin_name)
    data_origin = odm.DataOrigin.objects(name__contains=origin_name).first()
    arquivo = OSCILOSCOPIO_DIR+'osciloscopio.csv'
    df = pd.read_csv(arquivo, delimiter=';')
    
    dt_timestart = datetime.datetime.strptime("22/07/29 14:17:11", "%y/%m/%d %H:%M:%S")
    #df = df.rename({'Time': 'date'})
    df = df.rename({'CH2(V)': 'PT-4801', 'CH7(V)': 'PT-4803'},axis=1)
    
    #df['date'] = dt_timestart+datetime.timedelta(seconds=df['Time'])
    df['date'] = df['Time'].apply(lambda linha: dt_timestart+datetime.timedelta(seconds=linha))
    list_tagnames = ['PT-4801', 'PT-4803']
    for tagname in list_tagnames:
        print("importando "+tagname)
        tag = odm.Tag(name=tagficator(tagname), original_name=tagname, data_origin=data_origin, description=tagname+" Osciloscópio").save()
        tagvar = odm.TagVar(tag = tag, name='val', unit='V').save()
        list_values = []
        def fill_values(row):
            list_values.append(odm.Values(tag_var=tagvar, val = row[tagname], date=row['date']))
        df[[tagname, 'date']].apply(fill_values, axis=1)    
        a = odm.Values.objects.insert(list_values)


#--NEW DATABASE
#drop_database()
#popular_origens()

#--SICA1_SQL
#import_sicasql_tags()
#create_sicasql_vars()
#import_sicasql_values()

#--SICA_TXT--
#import_sica_tags()
#create_sica_vars()
#import_sica_values()

#--OVATION--
#import_ovation()

#--SIMULADOR--
#import_simulador()
#import_simulador_ovation()

#--OSCILOSCOPIO--
#import_osciloscopio()



#--ANGRA1_DVR--
#import_dvr_tags()
#create_dvr_vars()
#import_dvr_runs()
#import_dvr_values()

# 

"""
test_origin()
import_vali_mea()

import_vali_dvr()

import_sica_tags()
update_tag_same_as()


import_sica_values()

normalizar_ue()
"""
#print(tagficator("                 - ACTUAL-EFF..IC//-..-   -._[.][..]a                                                                  "))

