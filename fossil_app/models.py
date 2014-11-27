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
    name = Column(String)
    ntype_id = Column(Integer)

    level_num = Column(Integer)
    level_code = Column(String)
    parent_id = Column(Integer)


class NodeType(db.Model):
    __tablename__ = 'nodetype'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class BioKingdom(db.Model):
    __tablename__ = 'biokingdom'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String)


class BioPhylum(db.Model):
    __tablename__ = 'biophylum'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String)


class BioClass(db.Model):
    __tablename__ = 'bioclass'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String)


class BioOrder(db.Model):
    __tablename__ = 'bioorder'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String)


class BioGenus(db.Model):
    __tablename__ = 'biogennus'

    id = Column(Integer, primary_key=True)
    ntype_id = Column(Integer)

    name = Column(String)
