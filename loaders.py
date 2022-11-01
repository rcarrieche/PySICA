import pyodbc 
import datetime
import pandas as pd
import odm
import os
from constantes import *
from pymongo import MongoClient
#from matplotlib import pyplot as plt
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

class ValiConnection(object):
 
    def __init__(self, **kwargs):
        self.server = 'localhost' 
        self.database = 'SICA1_SQL' 
        self.username = 'sa' 
        self.password = 'Vali1234'
        if (kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        self.cursor = self.conn.cursor
    
    def get_cursor(self):
        return self.cursor

class Loader(object):
    """ 
    Objetos responsáveis por usar as conexões e entregar os dados em formato dataframe aos datasets
    """
    
    def __init__(self):
        pass
    
    def get_tags(self):
        pass
    
    def get_tagvalues(self, list_tags):
        pass
    
    
class ValiLoader(Loader):
    """
    documentation
    """
    def __init__(self, **kwargs):
        self.vali_connection = ValiConnection(**kwargs) ## TODO: guardar as conexões em um método de classe
        self.cursor = self.vali_connection.cursor()
        print("iniciou ValiLoader")
        
    def change_database(self, database):
        """
        Parameters
        ----------
        database : TYPE str
            
        muda a conexão ao banco de dados

        Returns
        -------
        None.

        """
        self.vali_connection = ValiConnection(database = database) ## TODO: guardar as conexões em um método de classe
        self.cursor = self.vali_connection.cursor()
        
    def get_vali_mea(self, list_tags, inicio, fim):
        """ Retorna tupla resultados, colunas. Este será o padrão das consultas """
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(inicio, format_string)
        dt_fim = datetime.datetime.strptime(fim, format_string)
        query = "SELECT TAG_DEF.PSC, MEA.Date_Acquisition, MEA.Value_Average FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC WHERE MEA.PSC IN {0} AND MEA.Date_Acquisition BETWEEN '{1}' AND '{2}'".format(str(tuple(list_tags)), dt_inicio.isoformat(), dt_fim.isoformat())
        #print(query)
        self.cursor.execute(query)
        #dados_mea = self.cursor.fetchall()
        '''
        dados_mea = []
        for linha in self.cursor.fetchall():
            print(linha)
            dados_mea.append(list(linha))
        '''
        # tentar da forma pytônica
        dados_mea = [list(linha) for linha in self.cursor.fetchall()]
        colunas = [c[0] for c in self.cursor.description]
        df_mea = pd.DataFrame(dados_mea, columns = colunas)
        #df_mea.columns = colunas
        return df_mea
    
    
    
    def get_sica1sql_tags(self):
        self.change_database('SICA1_SQL')
        """
        Returns
        -------
        dados_tags : TYPE
            DESCRIPTION.
        colunas : TYPE
            DESCRIPTION.

        """
        query = """
            SELECT [PSC] ,[Description] ,[UE]
      FROM [SICA1_SQL].[dbo].[TAG_DEF]"""
        return self.execute_sql(query)
        
    
    def get_angra1dvr_tags(self):
        self.change_database('ANGRA1_DVR')
        query = """
            SELECT  Tags.TagID, Tags.Name, Tags.Comment, Tags.Consolidation, PhysUnits.Name as UE, Tags.PhysUnitID
  FROM [ANGRA1_DVR].[dbo].[Tags] left join 
  [ANGRA1_DVR].[dbo].[PhysUnits] on Tags.PhysUnitID = PhysUnits.PhysUnitID where Comment != ''
      """
        return self.execute_sql(query)
    
    # 3754 
    def get_runs(self):
        self.change_database('ANGRA1_DVR')
        query = """
            SELECT  *
            FROM [ANGRA1_DVR].[dbo].[Runs]
      """
        dados_runs, col_runs = self.execute_sql(query)
        #print(dados_runs, col_runs)
        query = "SELECT Tags.Name ,Runs.Run, sum (TagValues.Measurement) as Measurement FROM TagValues LEFT JOIN Tags on Tags.TagID = TagValues.TagID LEFT JOIN Runs  on Runs.Run = TagValues.Run where Tags.Comment = '' and Tags.Consolidation is null group by Runs.Run, Tags.Name order by Runs.Run asc, Tags.Name" 
        dados_runvalues, col_runvalues = self.execute_sql(query)
        col_values = []
        run_id_temp = 1
        dados_runs_final = []
        for run in dados_runs:
            run_data = run
            run_id = run[0]
            for rv in dados_runvalues:
                if (run_id_temp == run_id):
                    col_values.append(rv[0])
                if rv[1] > run_id: 
                    break
                elif rv[1] == run_id:
                    #print(run_data)
                    run_data.append(rv[2])
                    #print(run_data)
                
            dados_runs_final.append(run_data)
        col_runs = col_runs + col_values
        print(col_runs)
        return dados_runs_final, col_runs
        
        
    def get_sica1sql_values(self):
        self.change_database('SICA1_SQL')
        query = """
            SELECT TAG_DEF.PSC, MEA.Date_Acquisition, MEA.Value_Average 
            FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC 
            """
        #print(query)
        return self.execute_sql(query)
    

    
    def get_angra1dvr_ue(self):
        self.change_database('ANGRA1_DVR')
        query = "SELECT PhysUnitID ,[Name] FROM [PhysUnits]"
        #print(query)
        return self.execute_sql(query)
    
    def get_sica1sql_ue(self):
        self.change_database('SICA1_SQL')
        query = "SELECT distinct [UE] FROM [SICA1_SQL].[dbo].[TAG_DEF]"
        #print(query)
        return self.execute_sql(query)
    
    def execute_sql(self, query):
        self.cursor.execute(query)
        dados = [list(linha) for linha in self.cursor.fetchall()]
        colunas = [c[0] for c in self.cursor.description]
        return dados,colunas
        
    def get_angra1dvr_values(self, tagname=None, taglist = []):
        self.change_database('ANGRA1_DVR')
        query_resto = ""
        if tagname:
            query_resto = " and Tags.name='{0}'".format(tagname)    
        if taglist:
            lista_sql = str(taglist).replace('[', '(').replace(']', ')')
            query_resto = " and Tags.name in {0}".format(lista_sql)
        query = "SELECT  Tags.Name, Runs.Date, TagValues.* FROM TagValues left join Runs on TagValues.Run = Runs.Run left join Tags on TagValues.TagID = Tags.TagID WHERE Tags.Consolidation is not null {}".format(query_resto)
        print(query)
        return self.execute_sql(query)
        
    def get_vali_mea22222(self, list_tags, inicio, fim):
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(inicio, format_string)
        dt_fim = datetime.datetime.strptime(fim, format_string)
        query = "SELECT TAG_DEF.PSC,TAG_DEF.Description, TAG_DEF.UE, MEA.Date_Acquisition, MEA.Value_Average FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC WHERE MEA.PSC IN {0} AND MEA.Date_Acquisition BETWEEN '{1}' AND '{2}'".format(str(tuple(list_tags)), dt_inicio.isoformat(), dt_fim.isoformat())
        #print(query)
        self.cursor.execute(query)
        dados_mea = self.cursor.fetchall()
        colunas = [c[0] for c in self.cursor.description]
        resultados = []
        for linha in dados_mea:
            resultados.append(dict(zip(colunas, linha)))
        # print(colunas)
        return resultados
    
    def get_vali_dvr(self, list_tags, inicio, fim):
        """ Retorna tupla resultados, colunas. Este será o padrão das consultas """
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(inicio, format_string)
        dt_fim = datetime.datetime.strptime(fim, format_string)
        query = """SELECT TAG_DEF.PSC, MEA.Date_Acquisition, MEA.Value_Average FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC WHERE MEA.PSC IN {0} AND MEA.Date_Acquisition BETWEEN '{1}' AND '{2}'""".format(str(tuple(list_tags)), dt_inicio.isoformat(), dt_fim.isoformat())
        #print(query)
        self.cursor.execute(query)
        #dados_mea = self.cursor.fetchall()
        '''
        dados_mea = []
        for linha in self.cursor.fetchall():
            print(linha)
            dados_mea.append(list(linha))
        '''
        # tentar da forma pytônica
        dados_mea = [list(linha) for linha in self.cursor.fetchall()]
        colunas = [c[0] for c in self.cursor.description]
        df_mea = pd.DataFrame(dados_mea, columns = colunas)
        #df_mea.columns = colunas
        return df_mea


class SicaLoader(Loader):
    def __init__(self, **kwargs):
        pass
    def get_sica_tags(self, file_path): 
        pass
    def read_sica_file(self, file_path):
        arquivo = pd.read_fwf(file_path)
        print(arquivo)
        mongo_loader = MongoLoader(database = MONGO_DATABASE)
        
    def read_sica_tags(self, file_path):
        arquivo = pd.read_fwf(file_path)
        return arquivo
    def read_sica_batch(self, dir_path):
        """
        #aqui reaproveitamos o código legado
        leituras = []
        # caminhos = ["D:\\ValiScheduler\\dados SICA\\07052020", "D:\\ValiScheduler\\dados SICA\\09112019", "D:\\ValiScheduler\\dados SICA\\16072020", "D:\\ValiScheduler\\dados SICA\\25052019"]
        
        # caminhos = ["D:\ValiScheduler\dados SICA\HD valves november"]
        #caminhos = ["D:\ValiScheduler\dados SICA\FW data last"]
        caminhos = ["D:\ValiScheduler\dados SICA\Dados SICA 2021-03-04"]
        
        
        for caminho in caminhos:
            arquivos = os.listdir(caminho)
            for arquivo in arquivos:
                l = ps.read_sica_runs(caminho+"\\"+arquivo)
                leituras = leituras + l
                pass
        """
        
        # Ou fazer assim:
        dados_sica = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                     print(os.path.join(root, file))
                     dados_sica.append(self.read_sica_file(file))
        return dados_sica

class MongoLoader(Loader):  # acho que nem precisa disto, basta usar direto o pymongo e abrir a conexão no __init__
    def __init__(self, **kwargs):
        self.connection = MongoConnection(**kwargs) ## TODO: guardar as conexões em um método de classe
        self.db = self.connection.db
        
    def drop_database_test(self, database):
        # TODO: 
        self.connection.connection.drop_database(database)
        
    def get_tags(self, tagname_list, **kwargs):
        tags_qs = odm.Tag.objects(name__in = tagname_list, **kwargs)
        return tags_qs
        
    def get_values(self, tag_list, **kwargs):
        pass
    
class OLDMongoLoader(Loader):  # acho que nem precisa disto, basta usar direto o pymongo e abrir a conexão no __init__
    def __init__(self, **kwargs):
        self.connection = MongoConnection(**kwargs) ## TODO: guardar as conexões em um método de classe
        self.db = self.connection.db
        
    def drop_database_test(self, database):
        # TODO: 
        self.connection.connection.drop_database(database)
        
    def get_tags(self, tagname_list, **kwargs):
        tags_qs = odm.Tag.objects(name__in = tagname_list, **kwargs)
        return tags_qs
        
    def get_values(self, tag_list, **kwargs):
        pass
    
    

class PepseLoader(Loader):
    pass 

class UprateFilesLoader(Loader):
    #TODO: ORGANIZAR os dados no arquivo
    pass



loader = SicaLoader()


"""
loader = MongoLoader(database='Teste2')
tags = loader.get_tags(['PI1980A', 'PI1981A', 'TE6540'])
print(tags)
for tag in tags:
    print("name: {}      origin: {}".format(tag.name, tag.data_origin.name))
    print("desc: {}".format(tag.description))
    print(tag.__dict__)
    try:
        print("UE  : {}".format(tag.ue.name))
        print("UE _id : {}".format(tag.ue))
    except Exception as e:
        print("Erro de referência!")
        print(e)
    print("")
    
"""