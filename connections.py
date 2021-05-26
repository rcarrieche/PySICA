import pyodbc 
import datetime
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

# TODO: renomear este arquivo para loaders.]
# TODO: separar connection de loader
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
