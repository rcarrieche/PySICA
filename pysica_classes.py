import pint 
import numpy as np
import loaders
import odm
import pandas as pd
from pymongo import MongoClient
from constantes import *
import datetime


#DEPRECATED
class Curva(object):
    def __init__(self, curva_id, **kwargs):
        #variáveis básicas
        self.curva_id = curva_id
        self.titulo = ""
        self.descricao = ""
        self.title = ""
        self.description = ""
        self.ndim = 0
        self.tags = []
        # self.x = np.array()
        # TODO: abstrair melhor essa merda
        self.ue = [] # vetor de ue de acordo com os tags
        ue = {'original': '', 'used': ''}
        self.val = None
        # self.tags_ = tag
        self.metadata = []
        metadata = {'x_tag': None, 'y_tag':None, 'z_tag':None, 'x_options':{}, 'y_options':{}, 'z_options':{}}
        self.x_values = np.Array()
        self.y_values = np.Array()
        self.z_values = np.Array()
        if(kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
                
    def set_values(self, list_tags, list_values):
        pass

# DEPRECATED        
class Tag(object):
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname
        self.tag_id = ""
        self.titulo = ""
        self.descricao = ""
        self.title = ""
        self.description = ""
        self.origem_id = ""
        self.ue_original = ""
        self.metadata = {}
        self.related_to = {} # tags relacionados tag_id: tag_obj
        self.belongs_to = {} # tag do componente pai tag_id: tag_obj
        self.same_as = {} # tag_id: tag_obj
        if(kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)



class Dataset(object):

    def __init__(self, name, list_tags, **kwargs):
        print("aa")
        self.name = name
        self.list_tags = list_tags
        """
        if self.list_tags:
            self.read_tags(list_tags)
            """
        self.schema = pd.DataFrame()
        self.data_par = pd.DataFrame()
        self.data_var = pd.DataFrame()

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
        print(list_ids)
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



class Dataset2(object):
    def __init__(self, name, list_tags, **kwargs):
        self.titulo = ""
        self.dataset_id = dataset_id 
        self.origem_id = None # pra quando tiver origem
        #self.values = {}
        self.tags = {} # tag_id : Tag
        self.data = {} # tag_id : Curva 
        self.timesheet = []
        self.loader = None
        self.df = None
        if(kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)



    def update(self, **kwargs):
        if(kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        
    def load_vali_mea_df(self, list_tags, start, end):
        loader = loaders.ValiLoader(database = 'SICA1_SQL')
        df_mea = loader.get_vali_mea(list_tags, start, end)
        self.df = df_mea
        
        
    def load_vali_dvr(self, list_tags, start, end):
        loader = loaders.ValiLoader(database = 'ANGRA1_DVR')
        df_mea = loader.get_vali_mea(list_tags, start, end)
        self.df = df_mea
    
    def load_sica_file(self, list_tags, **kwargs):
        pass
        
    def register_tag(self, tag):
        self.tags.update({tag.tag_id:tag})
        print(self.tags)
        
    def get_tag_list(self):
        return self.tags.items()

    
    def get_val_dict(self, tag, **kwargs): # para satisfazer os testes agora. 
        # TODO: pensar em uma função melhor e padronizar os dados de retorno, lembrando que a organização do dataframe pertence ao objeto loader. O Dataset deve trabalhar com os dados já padronizados
        self.df.loc
        pass

    def get_timesheet(self):
        return
    
    def load_vali_mea222(self, list_tags, start, end): #TODO: de quem é a responsabilidade de 
        loader = loaders.ValiLoader()
        dados_mea = loader.get_vali_mea(list_tags, start, end)
        # print(dados_mea)
        valores = []
        tag_obj = None
        
        for dado_mea in dados_mea:
            tag_id = dado_mea['PSC']
            
            if tag_id not in self.tags: 
                # REGISTRA tag
                
                dados_tag = {
                    'titulo': dado_mea['Description'],
                    'origem_id': self.dataset_id,
                    'descricao': dado_mea['Description'],
                    'ue_original': dado_mea['UE']
                    }
                print(dados_tag)
                colunas_mantidas_tag = ['PSC', 'Description', 'UE']
                for col in colunas_mantidas_tag:
                    dados_tag.update({col: dado_mea[col]})
                tag_obj = Tag(tag_id, **dados_tag)
                self.register_tag(tag_obj)
            '''   
            if tag_id not in self.tags:
                 # reinicia inicia vetor de dados da curva para o tag
                valores = []
                self.tags.update({tag_id:tag_obj})
                '''
            valores.append(dado_mea['Value_Average'])
        # TODO: registrar os tags no dataset
        # TODO: registrar os dados 
    
    def load_tag(list_tags):
        pass

# não será feito dessa forma
class Head(Curva):
    pass



  
# DEPRECATED
class Tagval(object):
    val = '' # valor principal procurado, np array + pint
    tag = ''
    dados = '';
    def __init__(self, pysica_tag_obj, dados):
        tag = pysica_tag_obj
        dados = dados
    