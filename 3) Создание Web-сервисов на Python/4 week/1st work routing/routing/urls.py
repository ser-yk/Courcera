from django.conf.urls import url
from .views import simple_route, slug_route, sum_route, sum_get_method, sum_post_method


urlpatterns = {
    url(r'^routing/simple_route/(?P<something>\w*)$', simple_route),
    url(r'^routing/slug_route/(?P<slug>[a-z0-9-_]{1,16})\/$', slug_route),
    url(r'^routing/sum_route/(?P<arg1>[-\w]*)/(?P<arg2>[-\w]*)\/$', sum_route),
    url(r'^routing/sum_get_method/$', sum_get_method),
    url(r'routing/sum_post_method/', sum_post_method)
}
