# -*- coding: utf-8 -*-
import mongoengine as me

TAG_PROP = ['Measurement', 'Mea_Acc', 'Validated', 'Val_Acc']

class Run(me.Document): # compatibilidade com Vali para conversão
    run_id = me.IntField()
    date = me.DateTimeField()
    PDB = me.StringField()
    version = me.StringField()
    # TODO: procurar as propriedades do run na lista de tags e inserir tudo aqui em forma embedded
    
    

class UE(me.Document):
    name = me.StringField()
    ue_id = me.SequenceField()
    same_as = me.ReferenceField('UE')
    cannonical = me.StringField()
    
class TagType(me.Document):
    """
        Tipos: component, stream, measurement, run_info, value 
    """
    name = me.StringField()
    tagtype_id = me.SequenceField()

class TagProp(me.Document):
    """
        Universal tag properties 
    """
    name = me.StringField()
    tagprop_id = me.SequenceField()

class Tag(me.Document):
    #tagname = me.StringField()
    name = me.StringField()
    alt_names = me.ListField(me.StringField())
    tag_id = me.SequenceField()
    description = me.StringField()
    comment = me.StringField()
    tag_parent = me.ListField(me.ReferenceField('Tag'))
    tag_same_as = me.ListField(me.ReferenceField('Tag'))
    tag_sibling = me.ListField(me.ReferenceField('Tag'))
    tag_master = me.ReferenceField('Tag')
    tag_connections = me.ListField(me.ReferenceField('Tag'))
    ue = me.ReferenceField(UE)
    tagtype = me.ReferenceField(TagType)
    tag_properties = me.ReferenceField(TagProp)
    origin = me.ReferenceField('DataOrigin')
    kks = me.StringField()
    

class DataOrigin(me.Document):
    name = me.StringField()
    data_origin_id = me.SequenceField()
    description = me.StringField()
    related_docs = me.ListField()

class Dataset(me.Document):
    name = me.StringField()
    dataset_id = me.SequenceField()
    description = me.StringField()
    data_origin = me.ReferenceField(DataOrigin)

class Val(me.DynamicDocument):
    pass

class TagVal(me.Document):
    tag = me.ReferenceField(Tag)
    date = me.DateTimeField()
    dataset = me.ReferenceField(Dataset)
    #val = me.EmbeddedDocumentField(Val)
    val = me.DictField()
    
    
    
class Component(me.Document):
    name = me.StringField() 
    data_origin_id = me.SequenceField()
    description = me.StringField()
    related_docs = me.ListField()
    meta = {}
    
    