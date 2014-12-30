#coding=utf-8

import json
from functools import update_wrapper

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import six
from django.shortcuts import render
from django.utils.decorators import classonlymethod
from django.views.generic import View

from fossil_app.models import *
from fossil_app.db_util import *

# Create your views here.
class BaseView(View):
    def __init__(self, request, **kwargs):
        self.request = request
        self.method = request.method.lower()
        self.db = request.db
        self.user = request.user
        self.GET = self.request.GET
        self.POST = self.request.POST
        for key, value in six.iteritems(kwargs):
            try:
                setattr(self, key, int(value))
            except:
                setattr(self, key, value)

    @classonlymethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls(request, **kwargs)

            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            if self.method in self.http_method_names and hasattr(self, self.method):
                resp = getattr(self, self.method)()
                if isinstance(resp, HttpResponse):
                    return resp
                elif isinstance(resp, (list, dict)):
                    return HttpResponse(json.dumps(resp), content_type="application/json")
                elif isinstance(resp, (basestring, int)):
                    return HttpResponse(resp)
                else:
                    return HttpResponse()
            return self.http_method_not_allowed(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())
        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view


class FossilHomeView(BaseView):
    def get(self):
        tree = {'data':[{'text':"P1"}]}
        tree = Node.mk_child_tree(1)
        return render(self.request,\
                             "fossil_app/home.html", {'tree_data':tree})


class FossilPlantView(BaseView):
    def get(self):
        tree = Node.mk_child_tree(2)
        tree = json.dumps(tree)
        return render(self.request,\
                             "fossil_app/fossilplant/test.html", {'tree_data':tree})


class FossilSelectView(BaseView):
    def get(self):
        sel_node = db.session.query(Node).get(self.node_id)
        rel_class = globals()[sel_node.node_type.name]
        rel_obj = rel_class.query.filter(rel_class.node_id==sel_node.id).one()

        # Prepare basic introduction
        if rel_obj.article_id:
            base_article = Article.query.get(rel_obj.article_id)
        else:
            base_article = None

        # Prepare child node introduction
        sub_articles = []
        for c_node in sel_node.child_node:
            c_obj = get_node_obj(c_node.id)
            if c_obj.article_id:
                article = Article.query.get(c_obj.article_id)
                sub_articles.append(article)

        # Prepare related pictures
        pic_l = []

        # child type list
        add_node_flag = True
        child_types = get_fossil_child_types(sel_node)
        if not child_types:
            add_node_flag = False

        return render(self.request,\
                      "fossil_app/fossilplant/fossil_node.html",\
                      {'base_article':base_article,\
                       'sub_articles':sub_articles,\
                       'add_node_flag':add_node_flag,\
                       'parent_node':sel_node,\
                       'types':child_types,\
                       'selnode':sel_node,\
                       })


class FossilAddNodeView(BaseView):
    def get(self):
        sel_node = db.session.query(Node).get(self.node_id)

        # child type list
        child_types = get_fossil_child_types(sel_node)

        return render(self.request,\
                      "fossil_app/fossilplant/modal_body_add_node.html",\
                      {
                       'parent_node':sel_node,\
                       'types':child_types,\
                       })

    def post(self):
        parent_node = Node.query.get(self.POST['fPId'])
        node_type = NodeType.query.get(self.POST['fTId'])
        parent_id = int(self.POST['fPId'])
        ntype_id = int(self.POST['fTId'])
        new_name = self.POST['fName']
        new_name_cn = self.POST['fNameCN']

        # TODO
        # Combine Node() and NewNodeObj() into class method or into
        # a single function
        new_node = Node(new_name, new_name_cn, ntype_id, parent_id)
        db.session.add(new_node)
        db.session.flush()
        new_obj = create_node_obj(node_type, new_node)
        db.session.add(new_obj)

        tree = Node.mk_child_tree(2)
        tree = json.dumps(tree)

        return tree