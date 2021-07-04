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
    tagname = me.StringField()
    tag_id = me.SequenceField()
    description = me.StringField()
    comment = me.StringField()
    alt_name = me.ListField()
    tag_parent = me.ListField(me.ReferenceField('Tag'))
    tag_same_as = me.ListField(me.ReferenceField('Tag'))
    tag_sibling = me.ListField(me.ReferenceField('Tag'))
    ue = me.ReferenceField(UE)
    tagtype = me.ReferenceField(TagType)
    tag_properties = me.ReferenceField(TagProp)
    
class Dataset(me.Document):
    name = me.StringField()
    dataset_id = me.SequenceField()
    description = me.StringField()

class TagVal(me.Document):
    tag = me.ReferenceField(Tag)
    date = me.DateTimeField()
        