from django.contrib import admin
from .models import LeaveRequest, LeaveType

admin.site.register(LeaveRequest)
admin.site.register(LeaveType)
