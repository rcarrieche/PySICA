import pyodbc 
import datetime
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

# TODO: renomear este arquivo para loaders.]
# TODO: separar connection de loader
class ValiConnection(object):
    """
        teste docs
    """
    def __init__(self, **kwargs):
        self.server = 'localhost' 
        self.database = 'SICA1_SQL' 
        self.username = 'sa' 
        self.password = 'Vali1234' 
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        self.cursor = self.conn.cursor
    
    def cursor(self):
        return self.cursor

class Loader(object):
    """ 
    Objetos responsáveis por usar as conexões e entregar os dados em formato dataframe aos datasets
    """
    
    def __init__(self):
        pass
    
class ValiLoader(Loader):
    def __init__(self):
        vali_connection = ValiConnection() ## TODO: guardar as conexões em um método de classe
        self.cursor = vali_connection.cursor()
        
    def get_vali_mea(self, list_tags, inicio, fim):
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
    
    def get_vali_mea2(self, list_tags, inicio, fim):
        """ Retorna tupla resultados, colunas. Este será o padrão das consultas """
        format_string = '%Y-%m-%d %H:%M:%S'
        dt_inicio = datetime.datetime.strptime(inicio, format_string)
        dt_fim = datetime.datetime.strptime(fim, format_string)
        query = "SELECT TAG_DEF.PSC,TAG_DEF.Description, TAG_DEF.UE, MEA.Date_Acquisition, MEA.Value_Average FROM MEA LEFT JOIN TAG_DEF ON MEA.PSC = TAG_DEF.PSC WHERE MEA.PSC IN {0} AND MEA.Date_Acquisition BETWEEN '{1}' AND '{2}'".format(str(tuple(list_tags)), dt_inicio.isoformat(), dt_fim.isoformat())
        #print(query)
        self.cursor.execute(query)
        dados_mea = self.cursor.fetchall()
        colunas = [c[0] for c in self.cursor.description]
        return dados_mea, colunas

class SicaFileLoader(Loader):
    pass

    
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