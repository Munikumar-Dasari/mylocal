# Register your models here.
from django.contrib import admin
from .models import CreateLabel
from django.contrib import admin
from .models import *
from .models import Review



class imageAdmin(admin.ModelAdmin):
        list_display = ["Movie_name", "Poster", "get_date"]


admin.site.register(BoxOffice)
admin.site.register(CreateLabel)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(ProducerRegister)
admin.site.register(Movie)
admin.site.register(News)








