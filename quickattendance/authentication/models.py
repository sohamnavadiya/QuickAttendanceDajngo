# -*- coding: utf-8 -*-
import jwt

from datetime import datetime, timedelta, time

import qrcode
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.files import File
from django.db import models

from attendance.models import Attendance
from core.models import TimestampedModel


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_present_user(self, session_id, _status):
        return self.filter(is_active=True)\
            .select_related('profile')\
            .filter(id__in=Attendance.objects.filter(session_id=session_id, status='present'))

    def get_absent_user(self, session_id, _status):
        return self.filter(is_active=True)\
            .select_related('profile')\
            .exclude(id__in=Attendance.objects.filter(session_id=session_id, status='present'))


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    is_staff = models.BooleanField(default=False)

    qrcode = models.ImageField(upload_to=settings.QRS3BUCKET, blank=True, null=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def save(self, *args, **kwargs):
        # Generate qrcode before calling super.save
        super(User, self).save()
        self.generate_qrcode()

    def update(self, *args, **kwargs):
        super(User, self).save()

    def generate_qrcode(self):
        from django.conf import settings

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data({'id': self.id, 'username': self.username, 'email': self.email})
        qr.make(fit=True)

        filename = 'qrcode-%s.png' % self.id

        img = qr.make_image()
        bucket_path = settings.QRS3BUCKET + '/' + filename
        path = settings.MEDIA_ROOT + '/' +bucket_path
        print path

        img.save(path)

        # with open(path, "rb") as reopen:
        #     django_file = File(reopen)
        #     self.qrcode.save(filename, django_file, save=False)

        user_obj = User.objects.get(id=self.id)
        user_obj.qrcode = bucket_path
        self.qrcode = bucket_path
        user_obj.update()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email +""+ self.id

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
      This method is required by Django for things like handling emails.
      Typically, this would be the user's first and last name. Since we do
      not store the user's real name, we return their username instead.
      """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        Here I dont want to set any expiration time
        """
        # dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
