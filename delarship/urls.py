from django.contrib import admin
from django.urls import path, include
from filebrowser.sites import site

urlpatterns = [
    path('filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('tinymce/', include('tinymce.urls')),
    path('webadm/', admin.site.urls),
    path('',include('appauth.urls')),
    path('',include('apiauth.urls')),
    path('',include('finance.urls')),
    path('',include('apifinance.urls')),
    path('',include('sales.urls')),
    path('',include('apisales.urls')),
    path('',include('delar.urls')),
    path('',include('apidelar.urls')),
    path('',include('ecom.urls')),
    path('',include('apiecom.urls')),
    path('',include('hrm.urls')),
    path('',include('apihrm.urls')),
]