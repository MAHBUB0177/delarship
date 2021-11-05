from django.db.models.fields import IntegerField
from sales.models import *
from django.db import connection, transaction
from django.db.models import Count, Sum, Avg, Max, Min
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from decimal import Decimal
from .validations import *
import logging
import sys
from django.utils import timezone
logger = logging.getLogger(__name__)
from django.db.models.functions import Cast
from django.db.models import FloatField, F, Func, Value, CharField, DateField
from appauth.models import Report_Table_Tabular, Report_Parameter, Query_Table