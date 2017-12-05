from attendance.models import SabhaSession, SabhaType, Attendance
from authentication.models import User

from authentication.serializers import UserSerializer

from authentication.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers

from profiles.models import Profile
from profiles.serializers import ProfileSerializer1, MentorSerializer


class SabhaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SabhaType
        fields = ('id', 'sabha_type')


class PostSabhaSessionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SabhaSession
        fields = ('id', 'user', 'sabhatype', 'date', 'status')


class GetSabhaSessionSerializer(DynamicFieldsModelSerializer):
    sabhatype = SabhaTypeSerializer(read_only=True)

    class Meta:
        model = SabhaSession
        fields = ('id', 'user', 'sabhatype', 'date', 'status')
        depth = 1


class AttendanceSerializer(serializers.ModelSerializer):
    # session_id = SabhaSessionSerializer(read_only=True)
    user = UserSerializer(read_only=True, fields=('username',))
    last_modified_by = UserSerializer(read_only=True, fields=('username',))

    # To change the key name in response
    session_info = GetSabhaSessionSerializer(read_only=True, source='session_id', fields=('id', 'sabhatype'))

    class Meta:
        model = Attendance
        fields = ('status', 'user', 'last_modified_by', 'session_info', 'leave_reason')
        # To add foreign key value info instead just primary key
        # depth = 1


class AttendanceInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('status', 'user', 'last_modified_by', 'session_id', 'leave_reason')
        # To add foreign key value info instead just primary key
        # depth = 1


class AttendanceAllDetail(serializers.ModelSerializer):
    profile = MentorSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')
