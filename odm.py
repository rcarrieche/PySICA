# -*- coding: utf-8 -*-
import mongoengine as me
import datetime
import odm_classes as ocl



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
    description = me.StringField()
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
    
   

class Dataset(me.Document):
    name = me.StringField()
    dataset_id = me.SequenceField()
    description = me.StringField()
    #data_origin = me.ReferenceField(DataOrigin)
    tag_list = me.ListField(me.ReferenceField('Tag'))
    var_list = me.ListField(me.ReferenceField('TagVar'))
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField(default=datetime.datetime.now())
    meta = {
        'allow_inheritance' : True
    }
    
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at=datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        return super(Dataset, self).save(*args, **kwargs)


class PropVal(me.EmbeddedDocument):
    tag = me.ReferenceField(Tag)
    val = me.FloatField()
    mea_unit = me.ReferenceField('EngUnit')


class ParVal(Values):
    tag = me.ReferenceField(Tag)
    val = me.FloatField()
    mea_unit = me.ReferenceField('EngUnit')
    
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
    
# upload das curvas 
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
    tag_ports = me.ListField(me.ListField(me.ReferenceField('Tag')))
    
#---------------------------------#

# classes do config
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

    

    



    