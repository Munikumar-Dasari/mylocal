from django.db import models
from django.forms import fields
from django import forms
from django.forms import Textarea
from django.forms import ModelForm
from .models import *

class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Privacy1
        fields = ['Heading', 'text']
        widgets = {
            "Text": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }

class TermsForm(forms.ModelForm):
    class Meta:
        model = Terms
        fields = ['Heading', 'text']
        widgets = {
            "Text": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }

class GuidelinesForm(forms.ModelForm):
    class Meta:
        model = Guidelines
        fields = ['Heading', 'text']
        widgets = {
            "Text": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }

