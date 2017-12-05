# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from django.db import models

from attendance.models import Attendance
from core.models import TimestampedModel


class ProfileManager(models.Manager):
    def mentor(self, mentor_id):
        return self.filter(mentor_id=mentor_id)


class Profile(TimestampedModel):
    objects = ProfileManager()

    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=20, blank=False)

    middle_name = models.CharField(max_length=20, blank=False)

    last_name = models.CharField(max_length=20, blank=False)

    mentor = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='mentor')

    updated_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='updated_by')

    # Each user profile will have a field where they can tell other users
    # something about themselves. This field will be empty when the user
    # creates their account, so we specify `blank=True`.
    bio = models.TextField(blank=True)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. Similar to `bio`, this field is not required. It may be blank.
    image = models.URLField(blank=True)

    # Birth date
    bod = models.DateField(null=True)

    contact_no = ArrayField(models.CharField(max_length=200), null=True)

    city = models.CharField(max_length=25, null=True)

    state = models.CharField(max_length=25, null=True)

    address = models.TextField(null=True)

    user_type = models.ForeignKey('Usertype', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserType(TimestampedModel):
    user_type = models.TextField(blank=False, unique=True)

    def __str__(self):
        return self.user_type
