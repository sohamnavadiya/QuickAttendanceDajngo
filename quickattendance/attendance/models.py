# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from core.models import TimestampedModel


class SabhaType(TimestampedModel):
    sabha_type = models.TextField(blank=False, unique=True)


class SabhaSessionManager(models.Manager):
    def session(self, sabha_type):
        return self.filter(status=sabha_type)


class SabhaSession(TimestampedModel):
    SABHA_SESSION_CHOICE = [
        ('active', 'active'),
        ('close', 'close'),
        ('pending', 'pending'),
        ('removed', 'removed'),
    ]

    objects = SabhaSessionManager()

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    sabhatype = models.ForeignKey('SabhaType', on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, default=SABHA_SESSION_CHOICE[0][0], choices=SABHA_SESSION_CHOICE)


class AttendanceSessionManager(models.Manager):
    def get_session_users(self, session_type):
        return self.filter(session_id=session_type)


class Attendance(TimestampedModel):
    ATTENDANCE_STATUS = [
        ('present', 'present'),
        ('absent', 'absent'),
        ('leave', 'leave'),
    ]

    objects = AttendanceSessionManager()

    class Meta:
        unique_together = ['session_id', 'user']

    session_id = models.ForeignKey('SabhaSession', on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='user')
    status = models.CharField(max_length=20, default=ATTENDANCE_STATUS[0][0], choices=ATTENDANCE_STATUS)
    last_modified_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='taken_by')
    leave_reason = models.TextField(blank=True, null=True)
