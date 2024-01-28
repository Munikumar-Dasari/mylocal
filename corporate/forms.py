from django import forms
from .models import *
from django.forms import Textarea


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['Name', 'Email', 'Subject', 'Message']
        widgets = {
            "Message": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }