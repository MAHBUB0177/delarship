from django.contrib import admin

# Register your models here.
from appauth.models import *

admin.site.register(Global_Parameters)
admin.site.register(Report_Configuration)
admin.site.register(Report_Parameter)
admin.site.register(Report_Parameter_Mapping)
admin.site.register(User_Settings)
admin.site.register(Branch)
admin.site.register(Employees)

