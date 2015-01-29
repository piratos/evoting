from django.contrib import admin
from blog.models import Condidate,Votant,evenement

admin.site.register(Votant)
admin.site.register(Condidate)
admin.site.register(evenement)
