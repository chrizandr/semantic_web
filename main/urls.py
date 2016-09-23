from django.conf.urls import url
from . import views
urlpatterns = [
    # /main/
    url(r'^$', views.index , name='index'),
    # /main/upload/
    url(r'^upload/$', views.uploads , name='upload'),
    url(r'^classes/$', views.classes , name = 'classes'),
    url(r'^instances/$', views.instances , name = 'instances')
]
