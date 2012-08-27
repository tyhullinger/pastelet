from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'pastelet.views.index', name='index'),
    url(r'^(?P<pastelet_id>.*)/$', 'pastelet.views.view', name='view'),
    url(r'^save', 'pastelet.views.save'),
)
