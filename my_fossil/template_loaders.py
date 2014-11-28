# -*- coding: utf-8 -*-
"""
See http://docs.djangoproject.com/en/dev/ref/templates/api/#using-an-alternative-template-language
Set https://gist.github.com/472309

To use:
* Add this template loader to settings: `TEMPLATE_LOADERS`
* Add template dirs to settings: `TEMPLATE_DIRS`

If in template debug mode - we fire the template rendered signal, which allows
debugging the context with the debug toolbar. Viewing source currently doesnt
work.

If you want {% url %} or {% csrf_token %} support I recommend grabbing them
from Coffin (http://github.com/dcramer/coffin/blob/master/coffin/template/defaulttags.py)
Note for namespaced urls you have to use quotes eg:
{% url account:login %} => {% url "account:login" %}
"""
import re, os, sys
from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist, Origin
from django.template.loader import BaseLoader
from django.utils.importlib import import_module
import jinja2
from jinja2 import evalcontextfilter, Markup, escape


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
        for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


class Template(jinja2.Template):
    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).render(context_dict)


# Get from django.template.loaders.app_directories.Loader
# At compile time, cache the directories to search.
fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir.decode(fs_encoding))

class App_Directoriesloader(BaseLoader):
    # whether the loader can be used in this Python installation.
    is_usable = True

    # Set up the jinja env and load any extensions you may have
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(app_template_dirs))
    env.template_class = Template

    # These are available to all templates.
    env.globals['BASE_URL'] = settings.BASE_URL
    env.globals['STATIC_URL'] = settings.STATIC_URL
    env.filters['nl2br'] = nl2br

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)
