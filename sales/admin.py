from django.contrib import admin

# Register your models here.

from sales.models import *

admin.site.register(Application_Settings)
admin.site.register(ShowRoom)
admin.site.register(EMI_Settings)
admin.site.register(Products_Price_Type)