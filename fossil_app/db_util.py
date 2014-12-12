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
