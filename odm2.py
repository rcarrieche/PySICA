# -*- coding: utf-8 -*-
import mongoengine as me

TAG_PROP = ['Measurement', 'Mea_Acc', 'Validated', 'Val_Acc']



class EngUnit(me.Document):
    name = me.StringField()
    unit_id = me.SequenceField()
    same_as = me.ReferenceField('EngUnit')
    cannonical_id = me.StringField()
    original_id = me.IntField()
    data_origin = me.ReferenceField('DataOrigin')    

class TagType(me.Document):
    """
        Tipos: component, stream, measurement, run_info, value 
    """
    name = me.StringField()
    tagtype_id = me.SequenceField()

class TagProp(me.DynamicDocument):
    """
        Universal tag properties 
    """
    name = me.StringField()
    tagprop_id = me.SequenceField()
    eng_unit = me.ReferenceField('EngUnit')

class Tag(me.Document):
    #tagname = me.StringField()
    name = me.StringField()
    alt_names = me.ListField(me.StringField())
    tag_id = me.SequenceField()
    original_id = me.IntField()
    description = me.StringField()
    comment = me.StringField()
    tag_parent = me.ListField(me.ReferenceField('Tag'))
    tag_same_as = me.ListField(me.ReferenceField('Tag'))
    tag_related = me.ListField(me.ReferenceField('Tag'))
    tag_master = me.ReferenceField('Tag')
    tag_connections = me.ListField(me.ReferenceField('Tag'))
    eng_unit = me.ReferenceField(EngUnit)
    tag_type = me.ReferenceField(TagType)
    tag_prop = me.ListField(me.ReferenceField(TagProp))
    data_origin = me.ReferenceField('DataOrigin')
    kks = me.StringField()
    meta = {
        'indexes' : ['name', 'data_origin' ]
    }

class DataOrigin(me.Document):
    name = me.StringField()
    data_origin_id = me.SequenceField()
    description = me.StringField()
    related_docs = me.ListField()
    parent_origin = me.ReferenceField('DataOrigin')


class Dataset(me.Document):
    name = me.StringField()
    dataset_id = me.SequenceField()
    description = me.StringField()
    data_origin = me.ReferenceField(DataOrigin)
    tag_list = me.ListField(me.ReferenceField('Tag'))


class PropVal(me.EmbeddedDocument):
    tag = me.ReferenceField(Tag)
    val = me.FloatField()
    eng_unit = me.ReferenceField('EngUnit')


    
# Descrição dos componentes    
class Component(me.Document):
    name = me.StringField() 
    data_origin_id = me.SequenceField()
    description = me.StringField()
    related_docs = me.ListField()
    meta = {}

# upload das curvas 
class Curve(me.Document):
    tags = me.ListField(me.ReferenceField(Tag))
    values = me.ListField(me.EmbeddedDocumentField(PropVal))
    
#---------------------------------#

# classes do config

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



    

    



    