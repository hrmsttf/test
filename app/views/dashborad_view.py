# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.views.employee_view import employees
from django.contrib.auth.decorators import login_required
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.forms.EmployeeForm import EmployeeForm 
from app.forms.LeaveTypeForm import LeaveTypeForm

#from app.forms import UserGroupForm  

from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
from app.models.leave_type_model import * 
from app.models.leave_balance import *
from app.models.department_model import *
from app.models.role_model import *
# from app.models.leave_balance_model import *
# from app.models import Group 

#from app.models import Group 
from django.conf.urls import url
from pprint import pprint
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q, query
from datetime import datetime
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse
import MySQLdb
from itertools import chain
from django.db.models import Prefetch
from django.db.models import Max, Subquery, OuterRef
from django.db import connection,transaction
from django.db.models import F
from app.models.employee_model import Employee , Work_Experience, Education, Dependent 
import datetime
from app.models.attendance_model import Attendance
from app.models.announcement_model import Announcement 

#from app.models import QuillModel

@login_required(login_url="/login/")
def index(request):
    query = Employee.objects.filter(role__is_active ='1', department__is_active ='1', birth_date= datetime.date.today() )

    # last 15 days records
    new_hires = Employee.objects.filter(is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=15))
   
    # last 3 records
    # new_hires = Employee.objects.filter(is_active = 1).order_by('-created_at')[:3]
    # print(new_hires)
    
    tdelta = 0
    myDate = datetime.date.today()
    check_in_time = Attendance.objects.filter(date=myDate, employee_id= request.user.emp_id)
    # print(check_in_time[0].checkin_time) 
    # t1 = request.session['checkin_session']
    if check_in_time:
        t1 = check_in_time[0].checkin_time.strftime('%H:%M:%S')

        if(check_in_time[0].checkout_time):
            if 'checkin_session' in request.session:
                t2 = datetime.datetime.now().strftime('%H:%M:%S')
            else:
                t2 = check_in_time[0].checkout_time.strftime('%H:%M:%S')
        else:
            t2 = datetime.datetime.now().strftime('%H:%M:%S')
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(t2, FMT) - datetime.datetime.strptime(t1, FMT)
        # print(tdelta)
        # check_in = tdelta.seconds/3600
        # print(check_in)

    announcements = Announcement.objects.filter(added_by__is_active = 1, created_at__lte=datetime.datetime.today(), created_at__gt=datetime.datetime.today()-datetime.timedelta(days=30)).order_by('-created_at')
    # print(announcements)
  
    context = {
        'birthdays':query,
        'check_in':tdelta,
        'new_hires':new_hires,
        'announcements':announcements
    }

    return render(request, "dashboard/dashboard.html", context)

    
