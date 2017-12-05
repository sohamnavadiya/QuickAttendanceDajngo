# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from attendance.models import SabhaType, SabhaSession, Attendance

admin.site.register(SabhaType)
admin.site.register(SabhaSession)
admin.site.register(Attendance)
