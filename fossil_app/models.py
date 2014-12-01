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
    name = Column(String(128))
    name_cn = Column(String(128))

    ntype_id = Column(Integer, ForeignKey('nodetype.id'))
    node_type = relationship("NodeType",\
                 backref=backref('node', cascade="all, delete", order_by=id))

    level_num = Column(Integer)
    level_code = Column(String(64))

    parent_id = Column(Integer, ForeignKey('node.id'), default=None)
    parent_node = relationship("Node", backref="child_node", remote_side="Node.id")

    def __init__(self, name, ntype_id, parent_id=None):
        self.name = name
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
    name = Column(String(128))

    def __init__(self, name):
        self.name = name

    def mk_node_data(self, node):
        node_data = {}
        node_data['text'] = node.name
        node_data['nodes'] = []

        return node_data

    def __repr__(self):
        return "<NodeType('%s')>" % self.name


class BioKingdom(db.Model):
    __tablename__ = 'biokingdom'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubOrder('%s')>" % self.name


class BioGenus(db.Model):
    __tablename__ = 'biogenus'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
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

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioSubGenus('%s')>" % self.name


class BioNotClear(db.Model):
    __tablename__ = 'bionotclear'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))

    def __init__(self, name, name_cn=None, ntype_id=None):
        self.name = name
        if name_cn:
            self.name_cn = name_cn
        if ntype_id:
            self.ntype_id = ntype_id

    def __repr__(self):
        return "<BioNotClear('%s')>" % self.name
