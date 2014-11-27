# -*- coding: utf-8 -*-
"""
flaskext.sqlalchemy
~~~~~~~~~~~~~~~~~~~

Adds basic SQLAlchemy support to your application.

:copyright: (c) 2012 by Armin Ronacher.
:license: BSD, see LICENSE for more details.
"""
import re
import weakref
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from django.conf import settings
from django.core import signals

_camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')


def _defines_primary_key(d):
    """Figures out if the given dictonary defines a primary key column."""
    return any(v.primary_key for k, v in d.iteritems()
        if isinstance(v, sqlalchemy.Column))


class _Model(object):
    """Baseclass for custom user models."""

    #: the query class used. The :attr:`query` attribute is an instance
    #: of this class. By default a :class:`BaseQuery` is used.
    query_class = orm.Query

    #: an instance of :attr:`query_class`. Can be used to query the
    #: database for instances of this model.
    query = None


class _BoundDeclarativeMeta(DeclarativeMeta):
    def __new__(cls, name, bases, d):
        tablename = d.get('__tablename__')

        # generate a table name automatically if it's missing and the
        # class dictionary declares a primary key. We cannot always
        # attach a primary key to support model inheritance that does
        # not use joins. We also don't want a table name if a whole
        # table is defined
        if not tablename and d.get('__table__') is None and\
           _defines_primary_key(d):
            def _join(match):
                word = match.group()
                if len(word) > 1:
                    return ('_%s_%s' % (word[:-1], word[-1])).lower()
                return '_' + word.lower()

            d['__tablename__'] = _camelcase_re.sub(_join, name).lstrip('_')

        return DeclarativeMeta.__new__(cls, name, bases, d)

    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key


class _QueryProperty(object):
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


class SQLAlchemy(object):
    def __init__(self, session_options=None):
        if session_options is None:
            session_options = {}

        self.session = self.create_scoped_session(session_options)
        self.class_registry = weakref.WeakValueDictionary()
        self.Model = self.make_declarative_base()

    @property
    def metadata(self):
        """Returns the metadata"""
        return self.Model.metadata

    def create_scoped_session(self, options=None):
        """Helper factory method that creates a scoped session."""
        return orm.scoped_session(orm.sessionmaker(**options))

    def make_declarative_base(self):
        """Creates the declarative base."""
        base = declarative_base(cls=_Model, name='Model',
            metaclass=_BoundDeclarativeMeta, class_registry=self.class_registry)
        base.query = _QueryProperty(self)
        return base

    def remove_decl_class(self, classname):
        try:
            self.class_registry.pop(classname)
        except KeyError:
            pass


db = SQLAlchemy(settings.MAIN_SESSION_OPTIONS)
signals.request_finished.connect(lambda **kwargs: db.session.remove)