from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Group)
admin.site.register(Patrol)
admin.site.register(Country)
admin.site.register(Game)
admin.site.register(Points)
admin.site.register(Subcamp)
admin.site.register(Setting)
