# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:53:45 2022

@author: nato
"""

import pint 
import numpy as np
#import loaders
#import odm
import pandas as pd
from pymongo import MongoClient
from constantes import *
import datetime
import odm


class Database(object):
    def get_origins(self):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)
        
        coll_tag = db.get_collection('tag')
        coll_origin = db.get_collection('data_origin')
        dados_origins = coll_origin.find()
        origins = []
        for origin in dados_origins:
            query_total_tags = {"data_origin":origin["_id"]}
            total_tags = len(list(coll_tag.find(query_total_tags)))
            origin.update({"total_tags":total_tags})
            origins.append(origin)
        return pd.DataFrame(origins)
    
    def get_tags(self, list_tag_ids = [], list_tag_names = [], list_origin_ids = [], associated_tags = False):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)

        
        coll_tag = db.get_collection('tag')
        coll_ue = db.get_collection('u_e')
        coll_origin = db.get_collection('data_origin')
        coll_tagval = db.get_collection("tag_val")
        
        query_tags = {"$or":[{"name":{"$in":list_tag_names}}, {"_id":{"$in": list_tag_ids}}, {"name":{"$in":list_tag_names}}]}
        if list_origin_ids:
            aaa = {"$and": [{"data_origin":{"$in":list_origin_ids}}]}
            query_tags.update(aaa)
        dados_tags = coll_tag.find(query_tags)
        tags = []
        for tag in dados_tags:
            #print(tag)
            ue = coll_ue.find_one({"_id":tag['ue']})
            origin = coll_origin.find_one({"_id":tag['data_origin']})
            total_values = len(list(coll_tagval.find({"tag":tag["_id"]})))
            tag.update({'ue':ue['name'], 'origin_name':origin['name'], 'total_values':total_values})
            tags.append(tag)
      
        return pd.DataFrame(tags)
    
    
    def get_tag(self, tag_id):
        pass
    
    def get_dataset(self, dataset_id):
        pass
    
    
    
    def get_datasets(self):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)
        datasets = odm.Dataset.objects()
        #print(datasets)
        #print(datasets.select_related())
        coll_tag = db.get_collection('tag')
        coll_dataset = db.get_collection('dataset')
        dados_dataset = coll_dataset.find()
        datasets = []
        for d in dados_dataset:
            list_tag_ids = []
            for t in d["tag_list"]:
                list_tag_ids.append(t)
            string_tags = "";
            query_tags = {"_id": {"$in":list_tag_ids}}
            dados_tags = coll_tag.find(query_tags)
            i = 0
            for t in dados_tags:
                string_tags = string_tags + " " + t["name"]+"\n"
                i = i+1
                #print(t)
                #print(string_tags)
            #d.update({"tags":string_tags})
            d.update({"tags":i})
            #print(d)
            #print(string_tags)
            #print(list_tag_ids)
            datasets.append(d)
        return pd.DataFrame(datasets)
        
    def import_tags(self, filename):
        pass
    
    def import_sica_tags(self, filename):
        pass
    
    def import_vali_tags(self, filename):
        pass
    
    def export_excel(self):
        pass
    

class Dataset(odm.Dataset):

    def __init__(self, name, list_tags=[], **kwargs):
        super(odm.Dataset, self).__init__(**kwargs)
        print("aa")
        #self.name = name
        #self.list_tags = list_tags
        """
        if self.list_tags:
            self.read_tags(list_tags)
            """
        self.schema = pd.DataFrame()
        self.data_par = pd.DataFrame()
        self.data_var = pd.DataFrame()
        self.data_run = pd.DataFrame()
    
    def insert_tags(self, list_tag_ids = [], tags=None):
        if not tags:
            tags = odm.Tag.objects(id__in=list_tag_ids)
        print(self.name)
        lista = list(self.tag_list)
        print(lista)
        lista = lista + list_tag_ids
        print(lista)
        self.tag_list = odm.Tag.objects(id__in=lista)
        self.save()
        
        pass
    
    def count_tags(self):
        pass
    
    def count_vars(self):
        pass
    
    def get_tags(self):
        pass
        
    # DEPRECATED
    def read_tags(self, list_tags = []):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)
        if(list_tags):
            self.list_tags.append(list_tags) 
        if not self.list_tags:
            print("Sem tags")
        
        coll_tag = db.get_collection('tag')
        coll_ue = db.get_collection('u_e')
        coll_origin = db.get_collection('data_origin')
        
        query_tag = {
            "name":{"$in":list_tags}, 
            "_id":{"$in": list_tags} }
        query_tags = {"$or":[{"name":{"$in":list_tags}}, {"_id":{"$in": list_tags}}]}
        dados_tags = coll_tag.find(query_tags)
        tags = []
        for tag in dados_tags:
            #print(tag)
            ue = coll_ue.find_one({"_id":tag['ue']})
            origin = coll_origin.find_one({"_id":tag['data_origin']})
            tag.update({'ue':ue['name'], 'origin_name':origin['name']})
            tags.append(tag)
      
        if self.schema.empty: 
            self.schema = pd.DataFrame(tags)
        else:
            self.schema.update(pd.DataFrame(tags))
        self.list_tags = tags
        return self.schema    

    def read_runs(self, list_datas = []):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)
        
        
        coll_run = db.get_collection('run')
        #coll_ue = db.get_collection('u_e')
        #coll_origin = db.get_collection('data_origin')
        # TODO: DATE_LIST DEVE SER VERificada se tem 2 valores (ini....cio e fim) ou mais de um valor (datas específicas)
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(list_datas[0], format_string)
        dt_fim = datetime.datetime.strptime(list_datas[1], format_string)
        query_run = {"$and":[{"date":{"$gte":dt_inicio}},{"date":{"$lte":dt_fim}}]}
        dados_runs = coll_run.find(query_run)
        runs = []
        for run in dados_runs:
            run.update(run['values'])
            runs.append(run)
      
        self.data_run = pd.DataFrame(runs)
        # cast types
        self.data_run['EXITCODE'] = self.data_run['EXITCODE'].astype('str')
        #self.data_run['NBAD'] = self.data_run['NBAD'].astype('Int64')
        #self.data_run['NFLAG'] = self.data_run['NFLAG'].astype('Int64')
        #self.data_run['date'] = pd.to_datetime(self.data_run['date'], format=format_string) 
        #self.data_run['date'] = pd.to_datetime(self.data_run['date']) 
        return self.data_run
    
    
    def add_tag(self, tag_id):
        self.list_tags.append(coll_tag.find())

    def remove_tags(self, list_tag_removed = []):
        busca_itens = self.schema["_id"].isin(list_tag_removed)
        self.schema = self.schema.loc[~busca_itens]



    def read_mongo_df(db, collection, query={}, no_id=False):
        """ Read from Mongo and Store into DataFrame """

        client = MongoClient()
        db = client.get_database(db)
        collection = db.get_collection(collection)
        # Make a query to the specific DB and Collection
        cursor = collection.find(query)
        
        # em algum ponto aqui vou ter que e

        # Expand the cursor and construct the DataFrame
        df =  pd.DataFrame(list(cursor))

        # Delete the _id
        if no_id:
            del df['_id']

        return df

    def load_data_var(self, list_datas):
        client = MongoClient()
        db = client.get_database(MONGO_DATABASE)
        if not self.list_tags:
            print("Sem tags")
        list_ids = [x["_id"] for x in self.list_tags]
        #print(list_ids)
        coll_tagval = db.get_collection('tag_val')
        coll_tag = db.get_collection('tag')
        coll_ue = db.get_collection('u_e')
        coll_origin = db.get_collection('data_origin')
        # TODO: DATE_LIST DEVE SER VERificada se tem 2 valores (inicio e fim) ou mais de um valor (datas específicas)
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(list_datas[0], format_string)
        dt_fim = datetime.datetime.strptime(list_datas[1], format_string)
        tags = []
        list_tag_values = []

        for t in self.list_tags:
            tag = t
            #ue = coll_ue.find_one({"_id":tag['ue']})
            ue = tag['ue']
            origin = coll_origin.find_one({"_id":tag['data_origin']})
            #tag.update({'ue':ue['name'], 'origin_name':origin['name']})
            tag.update({'ue':ue, 'origin_name':origin['name']})
            query_tagval = {
                "tag":tag["_id"]
            # ,"date":{"$and":[{"$gte":dt_inicio},{"$lte":dt_fim}]}
            ,"$and":[{"date":{"$gte":dt_inicio}},{"date":{"$lte":dt_fim}}]
                #,"date":{"$gte":dt_inicio}
                #,"date":{"$lte":dt_fim}
            }
            dados_tagval = coll_tagval.find(query_tagval)
            valores = []
            count_none = []
            for dado in dados_tagval:
                try:
                    val = {"date": dado["date"], "val":dado["val"], "name": tag["name"], "origin": tag["origin_name"], "tag_id": tag["_id"]}
                    val.update(dado["values"])

                except KeyError as e:
                    count_none.append(dado)
                    pass
                valores.append(val)

            list_tag_values = list_tag_values+valores    
        #print(list_tag_values)
        self.data_var = pd.DataFrame(list_tag_values)
        return self.data_var





    