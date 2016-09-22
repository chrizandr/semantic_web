from django import forms
from .models import Owl

class OwlForm(forms.ModelForm):
    class Meta:
        model = Owl
        fields = [
            "OWLfile",
        ]
