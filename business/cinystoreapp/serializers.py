from cinystore import settings
from rest_framework import serializers
from cinystoreapp.models import *
from business.models import *
from podadmin.models import *
from labels.models import *
from corporate.models import *

 
class CreatelabelSerializer(serializers.ModelSerializer):
    class Meta : 
        model = CreateLabel
        fields = ['id','Movie_name','Language','Genre','Production_house','Producer','cast','Director','Music_director','Poster',
                  'Banner','Release_date','synopsis','trailer','Other_Languages',
                  'lyricist','choreographer','Script_writer','Running_Time','Maturity','Budget','Distribution',
                  'Recording_studio','Graphic_designer', 'like_count','follow_count','share_count','comment_count','timestamp_field','model_type']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model   = PostText1
        fields = ['Movie_name', 'Image', 'text', 'timestamp_field', 'like_count','follow_count', 'Heading', 'source']

class TmdbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id','movie_title', 'overview', 'release_date', 'poster_path','genre', 'language','video','producer','director','music_director'
                  ,'crew','cast','timestamp_field','like_count','follow_count','share_count','comment_count','model_type']

class MoviePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostText1
        fields = ['id','Movie_name', 'Image', 'text', 'timestamp_field', 'like_count','follow_count','share_count','comment_count','Heading','model_type']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Review
        fields = ['id','author', 'stars','Movie_name', 'comment', 'timestamp_field', 'like_count','share_count','comment_count','model_type']

class TrailerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CreateLabel
        fields = ['id','Movie_name','trailer','Poster','timestamp_field','like_count','share_count','model_type']

class ProducerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model =ProducerRegister
        fields = ['producer_id','production_house_image','production_house']


class tmdb_serializer_feedpage(serializers.ModelSerializer):
    poster_path = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_poster_path(self, obj):
        return settings.TMDB_LINK + str(obj.poster_path)
    
    def get_logo(self, obj):
        return settings.AWS_STORAGE_LINK + str(obj.logo)
    
    class Meta:
        model = Movie
        fields = ['id','movie_title','language','genre', 'overview', 'poster_path','timestamp_field','like_count','follow_count','share_count','comment_count','source','logo','model_type']

class createlabel_serializer_feedpage(serializers.ModelSerializer):
    Poster = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_Poster(self, obj):
        return obj.Poster.url

    def get_logo(self, obj):
        return settings.AWS_STORAGE_LINK + str(obj.logo)
    
    class Meta:
        model = CreateLabel
        fields = ['id', 'Movie_name','Language','Genre','Poster','synopsis','timestamp_field','like_count','follow_count','share_count','comment_count','source','logo','model_type']

class posttext_serializer_feedpage(serializers.ModelSerializer):
    Image = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_Image(self, obj):
        return obj.Image.url
    
    def get_logo(self, obj):
        return settings.AWS_STORAGE_LINK + str(obj.logo)
    
    class Meta:
        model = PostText1
        fields = '__all__'

class review_serializer_feedpage(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        return settings.AWS_STORAGE_LINK + str(obj.logo)
    
    class Meta:
        model = Review
        fields = ['id','Movie_name', 'author','comment', 'timestamp_field','like_count','share_count','comment_count','source','logo','model_type']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserInfo
        fields=['profilephoto','username','email','phone_number','first_name','last_name','website','date_of_birth',
                'country_name','state','city','company_brief','gender','facebook_account','twitter_account','spotify_account']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'phone_number': {'required': False},
        }
        
from marketing.models import Terms,Privacy1

class terms_serializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ['Heading','text','timestamp_field']


class privacy_serializer(serializers.ModelSerializer):
    class Meta:
        model = Privacy1
        fields = ['Heading', 'text', 'timestamp_field']

class ClipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clips
        fields = ['id','Heading','text','Movie_name','Video','Image','timestamp_field','like_count','comment_count','share_count','model_type']