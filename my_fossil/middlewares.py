# -*- coding: utf-8 -*-
import sys
import logging
import traceback
from django.http import HttpResponseServerError
from db_orm import db


class MiddleWareTpl(object):
    def __init__(self):
        pass

    def process_request(self, request):
        pass

    def process_view(self, request, view, args, kwargs):
        pass

    def process_response(self, request, response):
        pass

    def process_exception(self, request, exception):
        pass


class DatabaseMiddleware(object):
    """Sqlalchemy database object"""

    def process_request(self, request):
        request.db = db

    def process_response(self, request, response):
        try:
            request.db.session.commit()
        except Exception, e:
            logging.error(e)
            request.db.session.rollback()
        return response

"""
class ExceptionMiddleware(object):

    def process_exception(self, request, exc):
        print request
        print traceback.format_exc()

        if isinstance(exc, FSLException):
            message = '%d:%s' % (exc.errno, exc.message)
        else:
            message = str(exc)

        return HttpResponseServerError(message)
"""
