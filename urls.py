from django.conf.urls import patterns, include, url
from django.conf import settings
from django.template import Context, Template

t = Template('^{{ root }}/')
pattern = t.render(Context({ 'root': settings.ROOTAPP }))

urlpatterns = patterns('',
    url(pattern, include('organization.urls')),
)