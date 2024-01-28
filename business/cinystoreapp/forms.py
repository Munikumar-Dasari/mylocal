from django.db import models
from django.forms import fields
from .models import CreateLabel
from django import forms
from django.forms import Textarea
from .models import Review
from .models import *


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = CreateLabel
        fields = ('Movie_name','Language','Genre','Production_house','Producer','Director','Music_director','cast','Poster','Release_date','synopsis','trailer','Banner','Other_Languages','lyricist','choreographer','Script_writer','Running_Time','Maturity','Budget','Distribution','Recording_studio','Graphic_designer', 'Url_name', 'Singers', 'Editor', 'Cinematographer')
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
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'Movie_name', 'stars', 'review_date', 'comment']
        widgets = {
            "comment": Textarea(
                attrs={'rows':4, 'cols':100 }
            )

        }

class BoxOfficeForm(forms.ModelForm):
    class Meta:
        model = BoxOffice
        fields = ['Movie_name', 'production_house', 'movie_collections', 'day_collections', 'weekly_collections', 'month_collections']




class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['Movie_name', 'text', 'author']
        widgets = {
            "content": Textarea(
                attrs={'rows': 4, 'cols': 100}
            )
        }


