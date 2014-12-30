#coding=utf-8
import os

from django.conf import settings
from fossil_app.models import *

def add_node_type(name):
    nt = NodeType(name)
    db.session.add(nt)
    db.session.commit()


def get_node_obj(node_id):
    sel_node = db.session.query(Node).get(node_id)
    rel_class = globals()[sel_node.node_type.name]
    rel_obj = rel_class.query.filter(rel_class.node_id==sel_node.id).one()
    return rel_obj


def get_fossil_child_types(node):
    child_types = []
    if node.node_type.name == 'BioPhylum': # 门
        type_names = ['BioSubPhylum','BioClass']
    elif node.node_type.name == 'BioClass': # 纲
        type_names = ['BioSubClass', 'BioOrder', 'FossilSpecie']
    elif node.node_type.name == 'BioOrder': # 目
        type_names = ['BioSubOrder', 'BioFamily', 'BioGenus', 'FossilSpecie']
    elif node.node_type.name == 'BioFamily': # 科
        type_names = ['BioGenus', 'FossilSpecie']
    elif node.node_type.name == 'BioGenus': # 属
        type_names = ['FossilSpecie']
    else:
        type_names = []
    for tn in type_names:
        t = NodeType.query.filter(NodeType.name==tn and NodeType.tag=="fossil").one()
        child_types.append(t)
    return child_types


def create_node_obj(ntype, node):
    if ntype.name == 'BioPhylum':
        n_node_obj = BioPhylum(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioSubPhylum':
        n_node_obj = BioSubPhylum(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioClass':
        n_node_obj = BioClass(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioSubClass':
        n_node_obj = BioSubClass(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioOrder':
        n_node_obj = BioOrder(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioSubOrder':
        n_node_obj = BioSubOrder(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioFamily':
        n_node_obj = BioFamily(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioGenus':
        n_node_obj = BioGenus(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'BioSubGenus':
        n_node_obj = BioSubGenus(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    elif ntype.name == 'FossilSpecie':
        n_node_obj = FossilSpecie(node.name, node.id, name_cn=node.name_cn,
                               ntype_id=ntype.id)
    else:
        raise Exception("Wrong node type")
    return n_node_obj