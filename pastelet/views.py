from pastelet.models import Pastelet
from pastelet.models import PasteletForm

from pygments.lexers import get_all_lexers
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

def get_sorted_lexers():
    i = get_all_lexers()
    l = []

    for lexer in i:
        l.append("['" + lexer[1][0] + "','" + lexer[0] + "']")

    str = "[" + ', '.join(l) + "]"
    data = eval(str)
    data = sorted(data, key=lambda x: x[0])
    return data

def get_recent():
    recent = Pastelet.objects.order_by('-created')[:20]
    print recent[0].language
    return recent

def index(request):
    recent = get_recent()
    languages = get_sorted_lexers()
    form = PasteletForm()
    variables = RequestContext(request, {
        'form': form,
        'recent': recent,
        'languages': languages,
    })
    variables.update(csrf(request))
    return render_to_response('pastelet/index.html', variables)

def view(request, pastelet_id):
    recent = get_recent()
    p = get_object_or_404(Pastelet, url=pastelet_id)
    lexer = get_lexer_by_name(p.language, stripall=True)
    formatter = HtmlFormatter(linenos=True, cssclass="source")
    p.code = highlight(p.code, lexer, formatter)

    path = SITE_ROOT + "/static/css/code-style"
    files = os.listdir(path)
    tmp = []
    for file in files:
        tmp.append(file.replace('.css', ''))
    return render_to_response('pastelet/view.html', {'pastelet': p, 'styles': tmp, 'recent': recent})

def save(request):
    if request.method == 'POST':
        form = PasteletForm(request.POST)
        p = Pastelet()
        print request.POST

        print form.is_valid()
        print form.errors
        if form.is_valid():
            print 'the form is valid'
            obj = form.save()
            print obj.url
            return HttpResponseRedirect('/' + str(obj.url))
    return HttpResponseRedirect('/')
