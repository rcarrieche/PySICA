import pyodbc 
import datetime
from connections import ValiConnection, MongoConnection
import pandas as pd
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port


class Loader(object):
    """ 
    Objetos responsáveis por usar as conexões e entregar os dados em formato dataframe aos datasets
    """
    
    def __init__(self):
        pass
    
class ValiLoader(Loader):
    """
    documentation
    """
    def __init__(self, **kwargs):
        self.vali_connection = ValiConnection(**kwargs) ## TODO: guardar as conexões em um método de classe
        self.cursor = self.vali_connection.cursor()
        
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
        print(dados_runs, col_runs)
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
                    run_data.append(rv[2])
                
            dados_runs_final.append(run_data)
        col_runs = col_runs + col_values
        print(dados_runs_final)
        print(col_runs)
        
        
        
    def get_sica1sql_values(self):
        self.change_database('SICA1_SQL')
        query = """
            SELECT TAG_DEF.PSC, MEA.Date_Acquisition, MEA.Value_Average 
            FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC 
            """
        #print(query)
        return self.execute_sql(query)
    

    
    
    def get_angra1dvr_values(self):
        self.change_database('ANGRA1_DVR')
        query = """
            SELECT  
            FROM [ANGRA1_DVR].[dbo].[TagValues] left join [ANGRA1_DVR].[dbo].[PhysUnits] on Tags.PhysUnitID = PhysUnits.PhysUnitID 
            WHERE Comment != ''
            """
        #print(query)
        return self.execute_sql(query)
    
    def get_angra1dvr_ue(self):
        self.change_database('ANGRA1_DVR')
        query = """
            SELECT  Tags.TagID, Tags.Name, Tags.Comment, Tags.Consolidation, PhysUnits.Name as UE, Tags.PhysUnitID
            FROM [ANGRA1_DVR].[dbo].[Tags] left join [ANGRA1_DVR].[dbo].[PhysUnits] on Tags.PhysUnitID = PhysUnits.PhysUnitID 
            WHERE Comment != ''
            """
        #print(query)
        return self.execute_sql(query)
    
    def execute_sql(self, query):
        self.cursor.execute(query)
        dados = [list(linha) for linha in self.cursor.fetchall()]
        colunas = [c[0] for c in self.cursor.description]
        return dados,colunas
        
        
        
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
    
    def get_vali_dvr22222(self, list_tags, inicio, fim):
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
        pass


class MongoLoader(Loader):
    def __init__(self, **kwargs):
        self.connection = MongoConnection(**kwargs) ## TODO: guardar as conexões em um método de classe
        self.db = self.connection.db
        
    def drop_database_test(self, database):
        self.connection.connection.drop_database(database)

class PepseLoader(Loader):
    pass 

class UprateFilesLoader(Loader):
    #TODO: ORGANIZAR os dados no arquivo
    pass
    
loader = ValiLoader()
loader.get_runs()


'''
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()


cursor.execute("SELECT * from TAG_DEF") 
lista_tags = []
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()
    lista_tags.append(row)
    
print(lista_tags)
'''