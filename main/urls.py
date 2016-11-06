from django.conf.urls import url
from . import views

urlpatterns = [
    # Basic URLs for the various basic functions
    url(r'^$', views.index , name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.index, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^test/$', views.get_data_properties, name='test'),
    # Main link to upload and process OWL file
    url(r'^upload/$', views.OwlProcessor.as_view(), name='upload'),
]
