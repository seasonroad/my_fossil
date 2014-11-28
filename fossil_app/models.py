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
    parent_node = relationship("Node", backref="child", remote_side="Node.id")

    def __init__(self, name, ntype_id, parent_id):
        self.name = name
        self.ntype_id = ntype_id
        if parent_id:
            self.parent_id = parent_id

    def __repr__(self):
        return "<Node('%s')>" % self.name


class NodeType(db.Model):
    __tablename__ = 'nodetype'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<NodeType('%s')>" % self.name


class BioKingdom(db.Model):
    __tablename__ = 'biokingdom'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))


class BioPhylum(db.Model):
    __tablename__ = 'biophylum'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))


class BioClass(db.Model):
    __tablename__ = 'bioclass'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))


class BioOrder(db.Model):
    __tablename__ = 'bioorder'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))


class BioGenus(db.Model):
    __tablename__ = 'biogennus'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String(128))
    name_cn = Column(String(128))
