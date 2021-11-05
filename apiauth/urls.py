from django.urls  import path

from .views import *

urlpatterns = [
    path('apiauth-branch-api/', BranchApiView.as_view(), name='apiauth-branch-api'),
    path('apiauth-country-api/', Country_Api_View.as_view(), name='apiauth-country-api'),
    path('apiauth-employee-api/', Employee_Api_View.as_view(), name='apiauth-employee-api'),
    path('apiauth-applicationuser-api/', User_Settings_Api_View.as_view(), name='apiauth-applicationuser-api'), 
]

