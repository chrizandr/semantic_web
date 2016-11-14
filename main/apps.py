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
from __future__ import unicode_literals
from django.apps import AppConfig
# The main thread of the app, running as an application on the django server
class MainConfig(AppConfig):
    name = 'main'
