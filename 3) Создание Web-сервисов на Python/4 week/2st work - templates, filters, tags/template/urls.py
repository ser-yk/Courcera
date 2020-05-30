from django.conf.urls import url, include

from .views import echo, filters, extend

urlpatterns = [
    url(r'^echo/$', echo),
    url(r'^filters/$', filters),
    url(r'^extend/$', extend),
    url(r'^db/', include('db.urls')),
]
