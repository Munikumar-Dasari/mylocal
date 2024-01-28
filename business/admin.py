from django.contrib import admin

# Register your models here.

from .models import *
from cinystoreapp.models import ProducerRegister

admin.site.register(CorporateRegister)
admin.site.register(OttRegister)
admin.site.register(IndividualRegister)
admin.site.register(AgencyRegister)
admin.site.register(UserLikes)
admin.site.register(UserComments)
admin.site.register(UserShares)
admin.site.register(UserFollows)
admin.site.register(AbuseReport)
admin.site.register(NotInterested)
admin.site.register(ReportComments)
admin.site.register(PostText1)




