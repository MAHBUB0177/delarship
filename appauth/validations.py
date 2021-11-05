from .models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def fn_val_check_branch_exist(p_branch_code):
    if Branch.objects.filter(branch_code=p_branch_code).exists():
        return True
    else:
        return False
