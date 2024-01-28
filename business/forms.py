from django.db import models
from django.forms import fields
from .models import SubmitLabel, PostText1
from cinystoreapp.models import *
from django import forms
from django.forms import ModelForm, Textarea
from .models import SubmitClips, SubmitPost, SubmitLabel




class Submitform(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = SubmitLabel
        fields = ('Movie_name','Language','Genre','Production_house','Producer','Director','Music_director','cast',
                  'Poster','Release_date','synopsis','trailer','Banner','Other_Languages','lyricist','choreographer',
                  'Script_writer','Running_Time','Maturity','Budget','Distribution','Recording_studio','Graphic_designer', 
                  'Url_name', 'Singers', 'Editor', 'Cinematographer')
        widgets = {
            "synopsis": Textarea(
                attrs={'rows':4, 'cols':100 }
            )
        }
        Other_Languages = forms.CharField(required=False) 
        lyricist = forms.CharField(required=False)
        Singers = forms.CharField(required=False) 
        choreographer = forms.CharField(required=False) 
        Script_writer = forms.CharField(required=False) 
        Editor = forms.CharField(required=False) 
        Running_Time = forms.CharField(required=False) 
        Maturity = forms.CharField(required=False)
        Cinematographer = forms.CharField(required=False) 
        Graphic_designer = forms.CharField(required=False) 
        Distribution = forms.CharField(required=False) 
        Budget = forms.CharField(required=False) 
        Recording_studio = forms.CharField(required=False) 
        
class SubmitPostForm(forms.ModelForm):
    class Meta:
        model = SubmitPost
        fields = ['Heading','Movie_name','text','Image', 'Genre', 'Language']
        widgets = {
            "text": Textarea(
                attrs={'rows': 4, 'cols': 100}),
            #'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }		
	 

class VideoClipsForm(forms.ModelForm):
    class Meta:
        model = SubmitClips
        fields = ['Heading','text','Movie_name','Video','Image','Genre', 'Language']
        widgets = {
            "text": Textarea(attrs={'rows': 4, 'cols': 100}),
            'Movie_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WebseriesForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = WebSeriesLabel
        fields = ('webseries_name','Language','Genre','Production_house','Producer','Director','cast','Poster','Release_date','synopsis','trailer','season','episodes','streaming_on',)
        widgets = {
            "synopsis": Textarea(
                attrs={'rows':4, 'cols':100 }
            )

        }