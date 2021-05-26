import pint 
import numpy as np
import loaders





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

        
class Tag(object):
    def __init__(self, tag_name, **kwargs):
        self.tag_name = tag_name
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
    def __init__(self,dataset_id, **kwargs):
        self.titulo = ""
        self.dataset_id = dataset_id 
        self.origem_id = None # pra quando tiver origem
        #self.values = {}
        self.tags = {} # tag_id : Tag
        self.data = {} # tag_id : Curva 
        self.timesheet = []
        self.loader = None
        if(kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        
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
    def load_vali_mea(self, list_tags, start, end):
        loader = loaders.ValiLoader()
        df_mea = loader.get_vali_mea(list_tags, start, end)
        print(df_mea)
        dir(df_mea)
        
    def load_vali_dvr(self, list_tags, start, end):
        pass
    
    def load_sica_file(self, list_tags, **kwargs):
        pass
        
    def register_tag(self, tag):
        self.tags.update({tag.tag_id:tag})
        print(self.tags)
    def get_tag_list(self):
        return self.tags.items()




# não será feito dessa forma
class Head(Curva):
    pass

    
# DEPRECATED
class PysicaTagval(object):
    val = '' # valor principal procurado, np array + pint
    tag = ''
    dados = '';
    def __init__(self, pysica_tag_obj, dados):
        tag = pysica_tag_obj
        dados = dados
    