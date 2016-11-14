from django import forms
from .models import Owl
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class OwlForm(forms.ModelForm):
    class Meta:
        model = Owl
        fields = [
            "OWLfile",
        ]

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class Data_type_form(forms.Form):
    def __init__(self, *args, **kwargs):
        prop_object = kwargs.pop('prop_object')
        super(Data_type_form, self).__init__(*args, **kwargs)
        print prop_object
        for i, d_type in enumerate(prop_object):
            print d_type
            r_list=d_type[1]
            d_list=d_type[2]
            for each in r_list:
                if each=='integer':
                    self.fields['custom_%s' % i] = forms.IntegerField(label=d_type[0])
                elif each=='string':
                    self.fields['custom_%s' % i] = forms.CharField(label=d_type[0])
                elif each=='boolean':
                    self.fields['custom_%s' % i] = forms.BooleanField(label=d_type[0])
                elif each=='decimal':
                    self.fields['custom_%s' % i] = forms.DecimalField(label=d_type[0])
                elif each=='float':
                    self.fields['custom_%s' % i] = forms.FloatField(label=d_type[0])
                elif each=='double':
                    self.fields['custom_%s' % i] = forms.DecimalField(label=d_type[0])
                elif each=='duration':
                    self.fields['custom_%s' % i] = forms.DurationField(label=d_type[0])
                elif each=='dateTime':
                    self.fields['custom_%s' % i] = forms.DateTimeField(label=d_type[0], widget = forms.TextInput(attrs=
                {
                    'class': 'datepicker'
                }))
                elif each=='time':
                    self.fields['custom_%s' % i] = forms.TimeField(label=d_type[0])
                elif each=='date':
                    self.fields['custom_%s' % i] = forms.DateField(label=d_type[0])
                elif each=='anyURI':
                    self.fields['custom_%s' % i] = forms.URLField(label=d_type[0])
                else:
                    self.fields['custom_%s' % i] = forms.CharField(label=d_type[0])

    def data_values(self):
        for name,value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield(self.fields[name].label,value)
