from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
#    raise ValueError, "!! %s %s" % (request.path, urls)
    if request.path in ( reverse('wds.views.' + url) for url in urls.split() ):
        return '"active"'
    return '""'
