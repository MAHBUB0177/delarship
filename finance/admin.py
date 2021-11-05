from django.contrib import admin

# Register your models here.

from finance.models import *

admin.site.register(Application_Settings)
admin.site.register(Accounts_Balance)