#coding=utf-8
# 1 "../my_fossil/models.py"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "../my_fossil/models.py"
import os

from django.conf import settings
from django.shortcuts import render_to_response
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Text, DateTime, func, and_, select
from sqlalchemy.orm import relationship, backref, object_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from db_orm import db


class Node(db.Model):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))

    ntype_id = Column(Integer, ForeignKey('nodetype.id'))
    node_type = relationship("NodeType",\
                 backref=backref('node', cascade="all, delete", order_by=id))

    level_num = Column(Integer)
    level_code = Column(String(64))

    # TODO
    # enable obj_type, when we plan to add modern plants and animals
    # obj_type and node_type is different
    # obj_type: fossil/
    # node_type: the node level, like kindom/phylum/class
    #obj_type = Column(Integer)

    """
    SQLAlchemy One-to-Many relationship on single table inheritance - declarative
    http://stackoverflow.com/questions/6782133/sqlalchemy-one-to-many-relationship-on-single-table-inheritance-declarative
    """
    parent_id = Column(Integer, ForeignKey('node.id'), default=None)
    parent_node = relationship("Node", backref="child_node", remote_side="Node.id")

    def __init__(self, name, name_cn, ntype_id, parent_id=None):
        self.name = name
        self.name_cn = name_cn
        self.ntype_id = ntype_id
        if parent_id:
            self.parent_id = parent_id

    @classmethod
    def mk_child_tree(cls, node_id):
        node = cls.query.get(node_id)

        def mk_node_tree(node, tree=[]):
            cur_tree_node = node.node_type.mk_node_data(node)
            tree.append(cur_tree_node)
            for child_node in node.child_node:
                mk_node_tree(child_node, tree=cur_tree_node['nodes'])
        tree = []
        mk_node_tree(node, tree=tree)
        return tree

    def __repr__(self):
        return "<Node('%s')>" % self.name


class NodeType(db.Model):
    __tablename__ = 'nodetype'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))
    tag = Column(String(32))

    def __init__(self, name, name_cn, tag='fossil'):
        self.name = name
        self.name_cn = name_cn
        self.tag = tag

    def mk_node_data(self, node):
        """
        Maybe add different additional info for different types of nodes
        """
        node_data = {}
        node_data['text'] = node.name_cn
        node_data['node_id'] = node.id
        node_data['nodes'] = []

        return node_data

    def __repr__(self):
        return "<NodeType('%s')>" % self.name


class BioKingdom(db.Model):
    __tablename__ = 'biokingdom'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    note = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioKindom('%s')>" % self.name


class BioPhylum(db.Model):
    __tablename__ = 'biophylum'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioPhylum('%s')>" % self.name


class BioSubPhylum(db.Model):
    __tablename__ = 'biosubphylum'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubPhylum('%s')>" % self.name


class BioClass(db.Model):
    __tablename__ = 'bioclass'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioClass('%s')>" % self.name


class BioSubClass(db.Model):
    __tablename__ = 'biosubclass'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubClass('%s')>" % self.name


class BioOrder(db.Model):
    __tablename__ = 'bioorder'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioOrder('%s')>" % self.name


class BioSubOrder(db.Model):
    __tablename__ = 'biosuborder'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubOrder('%s')>" % self.name


class BioFamily(db.Model):
    __tablename__ = 'biofamily'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioFamily('%s')>" % self.name


class BioGenus(db.Model):
    __tablename__ = 'biogenus'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioGenus('%s')>" % self.name


class BioSubGenus(db.Model):
    __tablename__ = 'biosubGenus'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubGenus('%s')>" % self.name


class FossilSpecie(db.Model):
    __tablename__ = 'biofossilspecie'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)
    node_id = Column(Integer)

    name = Column(String(64))
    name_cn = Column(String(64))

    article_id = Column(Integer)
    fossil = relationship("Fossil", backref="specie")

    def __init__(self, name, node_id, name_cn=None, ntype_id=None):
        self.name = name
        self.node_id = node_id
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubGenus('%s')>" % self.name


class Fossil(db.Model):
    __tablename__ = 'fossil'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))
    name_cn = Column(String(64))

    owner = Column(String(64))

    country = Column(String(64))
    province = Column(String(64))
    city = Column(String(64))
    where = Column(String(64))

    geo_era = Column(String(64))
    geo_period = Column(String(64))
    geo_epoch = Column(String(64))
    geo_sys = Column(String(64))
    geo_ser = Column(String(64))
    geo_group = Column(String(64))

    text = Column(Text)
    pic_url = Column(String(64))
    pic_id = Column(Integer)
    pic_ids = Column(String(32))

    article_id = Column(Integer)
    specie_id = Column(Integer, ForeignKey('biofossilspecie.id'))

    def __init__(self):
        self.name = 'test'
        self.name_cn = '测试'
        self.owner = 'William'
        self.country = 'China'
        self.province = 'Beijing'
        self.city = '北京'
        self.where = "门头沟灰峪"

        self.geo_era = "中生代"
        self.geo_period = "石炭纪"
        self.geo_epoch = "早石炭"
        self.geo_sys = "石炭"
        self.geo_ser = "石炭"
        self.geo_group = "山西组"

        self.text = "这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子而已，这些只是为了测试一下子"
        self.pic_url = "data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw=="


class Article(db.Model):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    text = Column(Text)


class Picture(db.Model):
    __tablename__ = 'picture'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    dec = Column(String(512))
    url = Column(String(128))