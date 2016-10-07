from django.conf.urls import url
from . import views

urlpatterns = [
    # /main/
    url(r'^$', views.index , name='index'),
    # /main/upload/
    url(r'^upload/$', views.FormProcess.as_view() , name='upload'),
    url(r'^classes/$', views.FormProcess.as_view(template_name = 'main/classes.html') , name = 'classes'),
    url(r'^instances/$', views.instances , name = 'instances'),
    url(r'^form/$', views.getClasses , name = 'form'),
]
