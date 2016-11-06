from __future__ import unicode_literals
from django.db import models
import ontospy

class Owl(models.Model):
    OWLfile = models.FileField(upload_to='file_uploads/',null=True)
    timestamp = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.timestamp)

class GraphModel(models.Model):
    graph = ontospy.Graph
# Create your models here.
