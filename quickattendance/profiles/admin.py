# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from profiles.models import Profile, UserType

from django_otp.admin import OTPAdminSite
admin.site.__class__ = OTPAdminSite


admin.site.register(Profile)
admin.site.register(UserType)
