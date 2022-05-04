
import pandas as pd
from pymongo import MongoClient
import datetime
from pprint import pprint
from matplotlib import pyplot as plt
import pint 
import numpy as np
import seaborn as sns
ur = pint.UnitRegistry()
ur.load_definitions('C:\\Users\\nato\\Pysica\\dev\\add_units.txt')
import pysica

MONGO_DATABASE = 'Teste_1'





def read_tags(tag_list, date_list, data_origin_name = 'ANGRA1_DVR'):
    
    # tag_list = ['PI1980A', 'PI1981A']
    
    #tag_list = ['GOV-VALVES_DP', 'PCSG-STM-21_MASSF']
    #origens = ['SICA1_SQL', 'ANGRA1_DVR']
    
    
    format_string = '%Y-%m-%d %H:%M:%S'
    
    # TODO: DATE_LIST DEVE SER VERificada se tem 2 valores (inicio e fim) ou mais de um valor (datas específicas)
    dt_inicio = datetime.datetime.strptime(date_list[0], format_string)
    dt_fim = datetime.datetime.strptime(date_list[1], format_string)
    #print(dt_inicio)
    #print(dt_fim)
    
    client = MongoClient()
    db = client.get_database(MONGO_DATABASE)
    
    
    coll_tagval = db.get_collection('tag_val')
    coll_tag = db.get_collection('tag')
    coll_ue = db.get_collection('u_e')
    coll_origin = db.get_collection('data_origin')
    """
    pipeline = []
    
    query_filtro = {
        "$match": {}
        }
    
    query_project = {
        "$project": {}
        }
    """
    query_tag = {"name":{"$in":tag_list}}
    dados_tags = coll_tag.find(query_tag)
    #print(dados_tags)
    tags = []
    tag_values = {}
    for tag in dados_tags:
        #print(tag)
        ue = coll_ue.find_one({"_id":tag['ue']})
        origin = coll_origin.find_one({"_id":tag['data_origin']})
        tag.update({'ue':ue['name'], 'origin_name':origin['name']})
        
        query_tagval = {
            "tag":tag["_id"]
           # ,"date":{"$and":[{"$gte":dt_inicio},{"$lte":dt_fim}]}
           ,"$and":[{"date":{"$gte":dt_inicio}},{"date":{"$lte":dt_fim}}]
            #,"date":{"$gte":dt_inicio}
            #,"date":{"$lte":dt_fim}
            }
        
        dados_tagval = coll_tagval.find(query_tagval)
        valores = []
        tempos = []
        count_none = []
        for dado in dados_tagval:
            try:
                val = {"date": dado["date"], "val":dado["val"], "name": tag["name"], "origin": tag["origin_name"]}
                val.update(dado["values"])
            
                # redefindino val para o teste:
                # val = {'val':dado['val']}
                
            except KeyError as e:
               # print("{} -> sem val para tag {} de {}".format(dado["date"], tag["name"], tag["origin_name"]))
                #print(e)
                count_none.append(dado)
                pass
            valores.append(val)
            tempos.append(dado['date'])
            
        tag_values.update({tag["_id"]:valores}) 
        #tag['values'] = pd.DataFrame(valores)
        
        #tag['values'] = pd.concat([pd.DataFrame(tempos), tag['values']])
        #print(tempos)
        #tag['tempos'] = pd.DataFrame(tempos)
        tag['ue'] = ue['name']
        tags.append(tag)
        if(count_none): 
            print("{} sem val {}x".format(tag["name"], count_none))
        
    dfs = []
    for _id, v in tag_values.items():
        #print("{}   {}".format(_id, v))
        dataframe = pd.DataFrame(v)
        dfs.append(dataframe)
    # aqqui formata o dataframe
    df_tags = pd.DataFrame(tags) 
    #return df_tags, pd.concat(dfs), tag_values
    return df_tags, pd.concat(dfs)
    #return tags
    # print(result)
    

#df_valores = pd.DataFrame(tag_values)
#df_tags = pd.DataFrame(tags)
# print(df_valores)
#print(df_tags)

# TODO: fazer do jeito tosco mesmo, preciso terminar o protótipo essa semana. 
