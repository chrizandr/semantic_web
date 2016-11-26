##########################################################################################
## Semantic Web Form                                                                    ##
## Authors : Chris Andrew, Santhoshini Reddy                                            ##
## Email: chris.g14@iiits.in ; santhoshini.g14@iiits.in                                 ##
## Github: https://github.com/chrizandr ; https://github.com/Sanny26                    ##
###################################################################                     ##
## Description: This project was developed as part of the SEFP course at IIIT Sri City  ##
## All code is available for free usage for educational purposes                        ##
## Authors do not authorize commercial use of the source code                           ##
##########################################################################################

# Script defines the URL patterns that are observed on the request, and how to handle them

################### Imports ##################
from django.conf.urls import url
from . import views
import django.contrib.auth.views as auth_views
from django.contrib.auth.decorators import login_required

##################### Source ####################
#----------------------------------------------------------------------------------------
urlpatterns = [
    #-----------------------------------------------------------------
    # Basic index page for the application
    url(r'^$', views.index , name='index'),
    # Page to register a new user
    url(r'^register/$', views.register, name='register'),
    # Login page
    url(r'^login/$', auth_views.login,{'template_name': 'main/login.html'}, name='login'),
    # Logout URL, redirects to index
    url(r'^logout/$', auth_views.logout,{'template_name': 'main/index.html'}, name='logout'),
    # Page to change password
    url(r'^passwordchange/$', views.mylogin_required(auth_views.password_change),{'template_name': 'main/pchange.html'}, name='password_change'),
    # Page to give success response of change
    url(r'changedone/$', views.mylogin_required(auth_views.password_change_done),{'template_name': 'main/pdone.html'}, name='password_change_done'),
    # Main link to upload and process OWL file
    url(r'^upload/$', views.mylogin_required(views.OwlProcessor.as_view()), name='upload'),
    # Link to display all the graph files that the user has stored in the database
    url(r'^displayfiles/$',views.get_graph,name="displayfiles"),
    # Link to generate a RDF code for a given set of key value pairs
    url(r'^generate/$',views.generate_file,name="generate"),
    # Link to get the class tree for a given Graph object, fileid is primary key.
    url(r'^classes/(?P<fileid>\d+)$',views.mylogin_required(views.FormProcess.as_view()),name="classes")
]
