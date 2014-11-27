from functools import update_wrapper

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import six
from django.shortcuts import render
from django.utils.decorators import classonlymethod
from django.views.generic import View


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
        return render(self.request, "fossil_app/home.html", {})
