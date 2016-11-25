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

# Script defines the various forms used in the project in various pages

################### Imports ##################
from django import forms
from .models import Owl
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

##################### Source ####################
#----------------------------------------------------------------------------------------
# OWLForm: Class to generate the form to upload an OWL file
# It uses the Owl model from the "models" file.
class OwlForm(forms.ModelForm):
    #-----------------------------------------------------------------
    class Meta:
        model = Owl
        fields = [
            "OWLfile",
        ]
#----------------------------------------------------------------------------------------
# UserForm: Class to generate the form registering a new user
# It uses the in built User model from django.contrib.auth.models
class UserForm(UserCreationForm):
    #-----------------------------------------------------------------
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]
    #-----------------------------------------------------------------
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
#----------------------------------------------------------------------------------------
# UserForm: Class to generate the forms for various classes and properties dynamically
# Uses the "ddprop_object" dictionary to construct forms dynamically for vaiour input types
# Support input types of the form: integer, string, boolean, decimal, float, double, duration, dateTime, time, date, anyURI
class Data_type_form(forms.Form):
    #-----------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        class_list = kwargs.pop('class_names')
        dprop_object = kwargs.pop('dprop_object')
        oprop_object = kwargs.pop('oprop_object')
        super(Data_type_form, self).__init__(*args, **kwargs)
        count=0
        for ontoclass in class_list:
            self.fields['custom_q%s' % count ] = forms.CharField(label="break",help_text="new_set")
            self.fields['c_%s' % ontoclass] = forms.CharField(label=ontoclass,help_text="Class",widget = forms.TextInput(attrs={ 'placeholder': 'Class'}))
            count+=1
            for prop in oprop_object[ontoclass]:
                self.fields['o_%s' % prop[0]] = forms.CharField(label=prop[0],help_text="Object Property",widget = forms.TextInput(attrs={ 'placeholder': 'Object Property'}))
                count+=1
            for prop in dprop_object[ontoclass]:
                prop_range=prop[1]
                prop_name=prop[0]
                if prop_range=='integer':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.IntegerField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='string':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.CharField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='boolean':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.BooleanField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='decimal':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.DecimalField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='float':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.FloatField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='double':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.DecimalField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='duration':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.DurationField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='dateTime':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.DateTimeField(label=prop_name,help_text="Data Property", widget = forms.TextInput(attrs={'class': 'datepicker','placeholder': 'Data Property'}))
                elif prop_range=='time':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.TimeField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='date':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.DateField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                elif prop_range=='anyURI':
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.URLField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                else:
                    self.fields['d_%s_%s' % (prop_name , prop_range) ] = forms.CharField(label=prop_name,help_text="Data Property",widget = forms.TextInput(attrs={ 'placeholder': 'Data Property'}))
                count+=1
    #-----------------------------------------------------------------
    def data_values(self):
        for name,value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield(self.fields[name].label,value)
