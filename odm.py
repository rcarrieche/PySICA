# -*- coding: utf-8 -*-
import mongoengine as me
import datetime
import odm_classes as ocl
import pandas as pd
from mongoengine.queryset.visitor import Q
from bson.objectid import ObjectId


class MeaUnit(me.Document):
    name = me.StringField()
    unit_id = me.SequenceField()
    same_as = me.ReferenceField('MeaUnit')
    #cannonical_id = me.StringField()
    original_id = me.IntField()
    data_origin = me.ReferenceField('DataOrigin')  

class TagVar(me.Document):
    name = me.StringField()
    original_name = me.StringField()
    full_name = me.StringField()
    description = me.StringField()
    tagvar_id = me.SequenceField()
    tag = me.ReferenceField('Tag')
    unit = me.StringField()
    mea_unit = me.ReferenceField(MeaUnit)
    alias = me.ListField(me.StringField())
    value_ranges = me.DictField()
    stats = me.DictField()
    parent_var = me.ReferenceField('TagVar')
    related_vars = me.ListField(me.ReferenceField('TagVar'))
    data_origin = me.ReferenceField('DataOrigin') 
    categorical = me.BooleanField()
    meta = {
        'indexes' : ['tag']
    }
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(TagVar, self).save(*args, **kwargs)
    
class TagType(me.Document):
    """
        Tipos: component, stream, measurement, run_info, value 
    """
    name = me.StringField()
    tagtype_id = me.SequenceField()


class Tag(me.Document):
    #tagname = me.StringField()
    name = me.StringField()
    original_name = me.StringField() # sem taguificator
    alt_names = me.ListField(me.StringField())
    document = me.ReferenceField('Document')
    tag_id = me.SequenceField()
    original_id = me.IntField()
    description = me.StringField()
    comment = me.StringField()
    tag_parent = me.ListField(me.ReferenceField('Tag'))
    tag_same_as = me.ListField(me.ReferenceField('Tag'))
    tag_related = me.ListField(me.ReferenceField('Tag'))
    tag_siblings = me.ListField(me.ReferenceField('Tag'))
    tag_master = me.ReferenceField('Tag')
    tag_connections = me.ListField(me.ReferenceField('Tag')) # TODO: esclarecer melhor os campos. [{tag, kind, weight}]
    mea_unit = me.ReferenceField(MeaUnit)
    tag_types = me.ListField(me.StringField())
    data_origin = me.ReferenceField('DataOrigin')
    data = me.DictField()
    kks = me.StringField()
    labels = me.ListField(me.StringField())
    meta = {
        'indexes' : ['name', 'data_origin' ]
    }
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Tag, self).save(*args, **kwargs)

class DataOrigin(me.Document):
    name = me.StringField()
    
    #data_origin_id = me.SequenceField()
    description = me.StringField()
    #related_docs = me.ListField()
    parent_origin = me.ReferenceField('DataOrigin')
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    meta = {
        'queryset_class': ocl.DataOriginQuerySet
        }
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(DataOrigin, self).save(*args, **kwargs)

class Documento(me.Document):
    name = me.StringField()
    original_name = me.StringField()
    tags = me.ListField(me.ReferenceField('Tag'))
    data = me.DictField()
    metadata = me.DictField()
    #original_content = me.Binary()
    data_origin = me.ReferenceField('DataOrigin')
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Documento, self).save(*args, **kwargs)
    
    
    


class Values(me.Document):
    val = me.FloatField()
    valcat = me.StringField()
    #cat = me.String
    tag_var = me.ReferenceField(TagVar)
    tag = me.ReferenceField(Tag)
    date = me.DateTimeField()
    seq = me.IntField()
    #dataset = me.ReferenceField(Dataset)
    #val = me.EmbeddedDocumentField(Val)
    #values = me.DictField()
    run = me.ReferenceField('Run')
    meta = {
        'indexes' : ['tag_var', 'date']
    }
    
    
class SearchDate(me.Document):
    name = me.StringField()
    description = me.StringField()
    start = me.DateTimeField()
    end = me.DateTimeField()
    interval = me.IntField()
    fill_na = me.StringField()   

class Dataset(me.Document):
    name = me.StringField()
    dataset_id = me.SequenceField()
    description = me.StringField()
    #data_origin = me.ReferenceField(DataOrigin)
    tag_list = me.ListField(me.ReferenceField('Tag'))
    var_list = me.ListField(me.ReferenceField('TagVar'))
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    search_dates = me.ListField(me.ReferenceField(SearchDate))
    meta = {
        #'allow_inheritance' : True,
        'queryset_class': ocl.DatasetQuerySet
    }
    def __init__(self, *args, **kwargs):
        super(Dataset, self).__init__(*args, **kwargs)
        self.data_tags = self.get_tags()
        #self.data_par = pd.DataFrame()
        self.data_vars = self.get_vars()
        self.data_runs = self.get_runs()
        self.values = pd.DataFrame()
        self.info = pd.DataFrame()
        self.dates = self.get_search_dates()
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Dataset, self).save(*args, **kwargs)
    
    def teste(self, a=0):
        print(a)
        print(self.name)
        
    def get_tags(self):
        #print(self.tag_list)
        fields = ['name', 'description', 'vars']
        self.data_tags = pd.DataFrame([tag.to_mongo() for tag in self.tag_list])
        return self.data_tags
    
    def get_vars(self):
        self.data_vars = pd.DataFrame([var.to_mongo() for var in self.var_list])
        #self.data_vars['tag_name'] = pd.Series(Tag.objects(_id=self.data_vars['tag']).first())
        #self.data_vars['tag_name'] = self.data_vars['tag'].apply(lambda row: Tag.get(_id=row)['name'])
        #self.data_vars['data_origin_name'] = self.data_vars['tag'].apply(lambda row: DataOrigin.get(_id=row)['name'])
        return self.data_vars
    
    def get_info(self):
        self.info = pd.DataFrame.from_dict(self._data, orient='index')
        return self.info
    
    def get_runs(self):
        pass
    
    def save_tagvars(self):
        self.var_list = list(self.data_vars['_id'])
        self.save()
    
    def get_search_dates(self):
        sd = pd.DataFrame([date.to_mongo() for date in self.search_dates])
        self.dates = sd
        return self.dates
    
    def load_values(self, search_date_pos = 0):
        #if not self.dates or self.dates.empty(): 
        #   raise Exception("sem intervalo definido")
        qf = Q(tag_var__in=self.data_vars["_id"]) & Q(date__gte=self.dates['start'][search_date_pos]) & Q(date__lte=self.dates['end'][search_date_pos])
        values = Values.objects(qf)
        values_list = [val.to_mongo() for val in values]
        #values_list = [{'date':val['date'], 'val':val['val'], 'tag_var':val['tag_var']['description']} for val in values]
        dfval = pd.DataFrame(values_list)
        df2 = pd.pivot_table(dfval, columns='tag_var', index='date')
        def completa_nome(col_var_id):
            tagvar = TagVar.objects(id=ObjectId(col_var_id)).first()
            tag = Tag.objects(id=tagvar['tag']['id']).first()
            data_origin = DataOrigin.objects(id=tag['data_origin']['id']).first()
            nome_completo = ""+data_origin['name']+'.'+tag['name']+'.'+tagvar['name'] + '('+str(tagvar['unit'])+')'
            tagvar['full_name'] = nome_completo
            tagvar.save()
            return nome_completo
        colunas_novas = [completa_nome(ind[1]) for ind in df2.columns]
        df2.columns=colunas_novas
        print(df2.columns)
        df2 = df2.reset_index().resample('{}S'.format(self.dates['interval'][search_date_pos]), on='date').mean()
        self.values = df2
        return self.values
    
    def insert_tags(self, list_tag_ids = [], tags=None):
        if not tags:
            tags = Tag.objects(id__in=list_tag_ids)
        print(self.name)
        lista = list(self.tag_list)
        print(lista)
        lista = lista + list_tag_ids
        print(lista)
        self.tag_list = Tag.objects(id__in=lista)
        self.save()
        
    def populate_tag_list(self, list_tagnames): 
        list_tag_ids = []
        for name in list_tagnames:
            tags = Tag.objects((Q(name__icontains=name)|Q(original_name__contains=name))|Q(description__contains=name))
            #print(tags.values_list('name'))
            new_tag_ids = list(tags.values_list('id'))
            #print(new_tag_ids, type(new_tag_ids))
            list_tag_ids = list_tag_ids + new_tag_ids
        self['tag_list'] = list_tag_ids
        return self['tag_list']
    
    def populate_var_list(self, list_varnames, origem_list = None):
        #list_var = ['CXI6748', 'GOV1', 'GOV2', 'GOV3', 'GOV4', 'PI4695', 'PI4696', 'PI484', 'PI485', 'PI486', 'PIR08', 'PIR-08', '']
        if(origem_list):
            origens = DataOrigin.objects(name__in=origem_list)
        else:
            origens = DataOrigin.objects()
        variaveis = []
        for var in list_varnames:
            variaveis= variaveis + list(TagVar.objects(tag__in=self['tag_list'], description__contains=var, data_origin__in=origens) )
        self['var_list'] = variaveis
        return self['var_list']

# datas(dates) devem ser marcados como [start, end, interval_s]
    def set_date(self, list_date, name='', description=''):
        fdia = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')  
        #list_date = ['2022-09-22 00:00:00', '2022-09-23 00:00:00', 5]
        #description = "Teste dia 29/10/2022 5 min, 1 dia"
        start = fdia(list_date[0])
        end = fdia(list_date[1])
        interval = list_date[2]
        #interval = datetime.timedelta(minutes=dates[2]).seconds
        #search_dates = [{'start':datetime.datetime}]
        new_date = SearchDate(start=start, end = end, interval = interval, name=name, description=description).save()
        #aaa.save()
        #self.search_dates = 
        #self.update(push__search_dates = new_date)
        self.search_dates = [new_date]
    
    def filtro(self, exclude_list):
        filtro = (~ self.data_vars['description'].str.contains('\$') )& (~ self.data_vars['description'].str.contains('rabalho') )
        self.data_vars = self.data_vars[filtro]
        return self.data_vars
    
    #TODO: 
    def full_data_vars(self):
        # prara odm
        self.data_vars['tag_name'] = None
        self.data_vars['data_origin_name'] = None
        self.data_vars['mea_unit_name'] = None
        def fname(row): 
            name = None
            origin = None
            try: 
                tag = Tag.objects(id=row['tag']).first()
                #print(tag['name'], tag['data_origin']['name'])
                name = tag['name']
                origin = tag['data_origin']['name']
                mea_unit = MeaUnit.objects.get(id = row['mea_unit'])['name']
                print(name, origin, mea_unit)
            except Exception as e:
                name = None      
                origin = None
                tag = None
                mea_unit = None
                print(e)
                print(row)
            #dorigin = tag['data_origin']['name']
            #row['tag_name'] = name
            #row['data_origin_name'] = origin
            #print(row['data_origin_name'])
            #print(name, origin)
            return name, origin, mea_unit
        #df['tag_name'], df['data_origin_name'] = df.apply(fname, axis=1)
        a = self.data_vars.apply(fname, axis=1)
        #return a
        #df['tag_name'] = df['tag'] 
        self.data_vars['tag_name'] = a.apply(lambda row: row[0])
        self.data_vars['data_origin_name'] = a.apply(lambda row: row[1])
        self.data_vars[' mea_unit_name'] = a.apply(lambda row: row[2])
        return self.data_vars
    #TODO: 
        
    def full_data_tags(self):
        # prara odm
        self.data_tags['mea_unit_name'] = None
        self.data_tags['data_origin_name'] = None
        self.data_tags['total_vars'] = None
        def fname(row): 
            name = None
            origin = None
            mea_unit = None
            total_vars = 0
            
            try: 
                name = row['name']
                origin = DataOrigin.objects(id = row['data_origin']).first()['name']
                mea_unit = MeaUnit.objects(id = row['mea_unit']).first()['name']
                total_vars = TagVar.objects(tag=row['_id']).count()
            except Exception as e:
                name = None      
                origin = None
                tag = None
                mea_unit = None
                total_vars = 0
                print(e)
                print(row)
            try:
                origin = DataOrigin.objects(id = row['data_origin']).first()['name']
            except:
                pass
            #row['tag_name'] = name
            #row['data_origin_name'] = origin
            #print(row['data_origin_name'])
            #print(name, origin)
            return name, origin, mea_unit, total_vars
        #df['tag_name'], df['data_origin_name'] = df.apply(fname, axis=1)
        a = self.data_tags.apply(fname, axis=1)
        #return a
        #df['tag_name'] = df['tag'] 
        self.data_tags['tag_name'] = a.apply(lambda row: row[0])
        self.data_tags['data_origin_name'] = a.apply(lambda row: row[1])
        self.data_tags['mea_unit_name'] = a.apply(lambda row: row[2])
        self.data_tags['total_vars'] = a.apply(lambda row: row[3])
        return self.data_tags
    
    
    def update_taglist(self):
        self.var_list = list(self.data_vars['_id'])
        
      
        
        
class PropVal(me.EmbeddedDocument):
    tag = me.ReferenceField(Tag)
    val = me.FloatField()
    mea_unit = me.ReferenceField('EngUnit')


# FUTURE: sublasse dos valores 
'''
class ParVal(Values):
    tag = me.ReferenceField(Tag)
    val = me.FloatField()
    mea_unit = me.ReferenceField('EngUnit')
  '''

  
# Descrição dos componentes    
class Component(me.Document):
    name = me.StringField() 
    data_origin_id = me.SequenceField()
    description = me.StringField()
    related_docs = me.ListField()
    meta = {}



class Run(me.Document): # compatibilidade com Vali para conversão
    run_id = me.SequenceField()
    date = me.DateTimeField()
    PDB = me.StringField()
    version = me.StringField()
    original_id = me.IntField()
    values = me.DictField()
    # TODO: procurar as propriedades do run na lista de tags e inserir tudo aqui em forma embedded
    
# upload das curvas. Estender odm.Values??
class Curve(me.Document):
    tag_vars = me.ListField(me.ReferenceField(TagVar))
    name = me.StringField()
    description = me.StringField()
    values = me.DictField() # var_id: list_values  -- deve corresponder cada posição!
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Curve, self).save(*args, **kwargs)

class Connection(me.Document):
    name = me.StringField()
    description = me.StringField()
    labels = me.ListField(me.StringField())
    tag_list = me.ListField(me.ReferenceField('Tag'))
    tag_ports = me.ListField(me.ListField(me.DictField()))

    
#---------------------------------#

# classes do config
# TODO: Vai ser tudo 
"""
class ProcessoModificador(me.Document):
    pass

class Eto(me.Document):
    pass

class Pmd(ProcessoModificador):
    pass

class Pm(ProcessoModificador):
    pass

class Pmp(Pm):
    pass

class Pmi(Pm):
    pass

class Ppp(Pm):
    pass

class ListaSeletiva(me.Document):
    pass

class ListaMaterial(me.Document):
    pass

class SIT(me.Document):
    pass

class Documento(me.Document):
    pass



class Req(me.Document):
    pass



# ------ documentos --------

class Fluxograma(me.DynamicDocument):
    name = me.StringField()
    sincronia_id = me.StringField()
    
    pass

"""

    

    



    