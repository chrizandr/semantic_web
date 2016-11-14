from django.conf.urls import url
from . import views
import django.contrib.auth.views as auth_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # Basic URLs for the various basic functions
    url(r'^$', views.index , name='index'),
    #url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', auth_views.login,{'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'main/index.html'}, name='logout'),
    url(r'^passwordReset/$', auth_views.password_reset,{'template_name': 'main/passwordReset.html'}, name='passwordReset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done,{'template_name': 'main/passwordResetdone.html'}, name='password_reset_done'),
    url(r'^password_reset_confirm/$', auth_views.password_reset_confirm,{'template_name': 'main/passwordResetconfirm.html'}, name='password_reset_confirm'),
    url(r'^password_reset_complete/$', auth_views.password_reset_complete,{'template_name': 'main/passwordResetcomplete.html'}, name='password_reset_complete'),
    url(r'^passwordchange/$', views.mylogin_required(auth_views.password_change),{'template_name': 'main/pchange.html'}, name='password_change'),
    url(r'changedone/$', views.mylogin_required(auth_views.password_change_done),{'template_name': 'main/pdone.html'}, name='password_change_done'),
    url(r'^home/$', views.home, name='home'),
    url(r'^test/$', views.get_data_properties, name='test'),
    # Main link to upload and process OWL file
    url(r'^upload/$', views.mylogin_required(views.OwlProcessor.as_view()), name='upload'),
    url(r'^propertyform/$', views.mylogin_required(views.get_data_properties), name='upload'),
    #Urls for login and singup
    url(r'^register/$', views.register, name='register'),
]
