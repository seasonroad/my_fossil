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


class GeoEon(db.Model):
    """宙"""
    __tablename__ = 'geo_eon'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    name_cn = Column(String(64))
    start_ma = Column(String(16))
    end_ma = Column(String(16))


class GeoEra(db.Model):
    """代"""
    __tablename__ = 'geo_era'

    id = Column(Integer, primary_key=True)
    geoeon_id = Column(Integer, ForeignKey('geo_eon.id'))
    geoeon = relationship("GeoEon",\
                 backref=backref('geoera', cascade="all, delete", order_by=id))
    name = Column(String(32))
    name_cn = Column(String(64))
    start_ma = Column(String(16))
    end_ma = Column(String(16))


class GeoPeriod(db.Model):
    """纪"""
    __tablename__ = 'geo_period'

    id = Column(Integer, primary_key=True)
    geoera_id = Column(Integer, ForeignKey('geo_era.id'))
    geoera = relationship("GeoEra",\
                 backref=backref('geoperiod', cascade="all, delete", order_by=id))
    name = Column(String(32))
    name_cn = Column(String(64))
    start_ma = Column(String(16))
    end_ma = Column(String(16))


class GeoEpoch(db.Model):
    """世"""
    __tablename__ = 'geo_epoch'

    id = Column(Integer, primary_key=True)
    geoperiod_id = Column(Integer, ForeignKey('geo_period.id'))
    geoperiod = relationship("GeoPeriod",\
                 backref=backref('geoepoch', cascade="all, delete", order_by=id))
    name = Column(String(32))
    name_cn = Column(String(64))
    start_ma = Column(String(16))
    end_ma = Column(String(16))


class GeoSystem(db.Model):
    """系"""
    __tablename__ = 'geo_system'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    name_cn = Column(String(64))

#class GeoSeries(db.Model):
#    """统"""


class GeoGroup(db.Model):
    """岩层单位：群"""
    __tablename__ = 'geo_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    name_cn = Column(String(64))


class GeoFormation(db.Model):
    """岩层单位：组"""
    __tablename__ = 'geo_formation'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))


class Fossil(db.Model):
    __tablename__ = 'fossil'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))
    owner = Column(String(64))

    country_id = Column(Integer)
    province_id = Column(Integer)
    city_id = Column(Integer)
    where = Column(String(64))

    geo_era_id = Column(Integer)        #代
    geo_period_id = Column(Integer)     #纪
    geo_epoch_id = Column(Integer)      #世
    geo_group_id = Column(Integer)      #群
    geo_formation_id = Column(Integer)  #组

    desc = Column(Text)
    cover_pic_url = Column(String(64))
    pic_id = Column(Integer)
    pic_ids = Column(String(32))

    article_id = Column(Integer)
    specie_id = Column(Integer, ForeignKey('biofossilspecie.id'))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.name_cn = kwargs['name_cn']
        self.owner = kwargs['owner']
        self.country_id = kwargs['country_id']
        self.province_id = kwargs['province_id']
        self.city_id = kwargs['city_id']
        self.where = kwargs['where']
        self.geo_era_id = kwargs['geo_era_id']
        self.geo_period_id = kwargs['geo_period_id']
        self.geo_epoch_id = kwargs['geo_epoch_id']
        self.geo_group_id = kwargs['geo_group_id']
        self.geo_formation_id = kwargs['geo_formation_id']
        self.desc = kwargs['geo_formation_id']

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


class Country(db.Model):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))
    short_name = Column(String(8))


class Province(db.Model):
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))
    name_cn_short = Column(String(32))


class City(db.Model):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    name_cn = Column(String(64))


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    longitude = Column(String(32))
    latitude = Column(String(32))
    addr = Column(String(128))