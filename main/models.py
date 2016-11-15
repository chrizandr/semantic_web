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

# Script defines database models required for the application. Models defined as classes along with attributes

################### Imports ##################
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


################### Source ##################
# ----------------------------------------------------------------------------------------
# Owl : Class is the main model used to handle all OWL file uploads
# consists of File, timestamp and userid fields
class Owl(models.Model):
    OWLfile = models.FileField(upload_to='file_uploads/', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    fname = models.CharField(default="temp",max_length=20)
    userid = models.IntegerField(default=-1)

    # -----------------------------------------------------------------
    def __str__(self):
        return str(self.timestamp)
