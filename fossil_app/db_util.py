import os

from django.conf import settings
from fossil_app.models import *

def add_node_type(name):
    nt = NodeType(name)
    db.session.add(nt)
    db.session.commit()


def add
