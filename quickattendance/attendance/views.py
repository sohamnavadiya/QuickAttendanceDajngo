# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from profiles.models import Profile

from profiles.serializers import ProfileSerializer, UserSerializerAll
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from .models import SabhaType, SabhaSession, Attendance
from .serializers import SabhaTypeSerializer, AttendanceSerializer, AttendanceInsertSerializer, \
    GetSabhaSessionSerializer, PostSabhaSessionSerializer, AttendanceAllDetail
from rest_framework import generics, status


class SabhaTypeList(generics.ListCreateAPIView):
    # disable pagination
    pagination_class = None
    queryset = SabhaType.objects.all()
    serializer_class = SabhaTypeSerializer


class SabhaTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SabhaType.objects.all()
    serializer_class = SabhaTypeSerializer


class SabhaSessionList(generics.ListCreateAPIView):
    queryset = SabhaSession.objects.all()
    serializer_class = GetSabhaSessionSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = PostSabhaSessionSerializer
        return self.create(request, *args, **kwargs)


class SabhaSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SabhaSession.objects.all()
    serializer_class = GetSabhaSessionSerializer


class SabhaSessionByStatus(generics.ListAPIView):
    serializer_class = GetSabhaSessionSerializer
    # disable pagination
    pagination_class = None

    def get_queryset(self):
        """
        This view should return a list of all the sabha as determined by the sabhatype portion of the URL.
        """
        sabhatype = self.kwargs['sabhatype']
        return SabhaSession.objects.session(sabhatype)


class AttendanceList(APIView):
    serializer_class = AttendanceInsertSerializer

    def post(self, request):
        attendance_obj = request.data.get('attendance', [])

        for single_user in attendance_obj:
            session_id = single_user.get('session_id')
            user_id = single_user.get('user')

            # The create serializer, validate serializer, save serializer pattern
            # below is common and you will see it a lot throughout this course and
            # your own work later on. Get familiar with it.
            serializer = self.serializer_class(data=single_user)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except IntegrityError as error:
                print error
            except ValidationError as error:
                print error
                print serializer.data.get('session_id')
                print serializer.data.get('user_id')
                # In this case, if the Person already exists, its name is updated
                single_obj = Attendance.objects.get(session_id=session_id, user=user_id)
                serializer = AttendanceInsertSerializer(single_obj, data=single_user)
                if serializer.is_valid():
                    print "Update existing attendance model."
                    serializer.save()

        return Response({"message": "Attendance stored successfully."}, status=status.HTTP_201_CREATED)


class AttendanceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceDetail(generics.ListAPIView):
    pagination_class = None
    serializer_class = AttendanceSerializer
    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        """
        This view should return a list of all the USERS of particular session.
        """
        session_id = self.kwargs['session_id']
        return Attendance.objects.get_session_users(session_id)


class AttendanceReportByStatus(generics.ListAPIView):
    pagination_class = None
    serializer_class = AttendanceAllDetail

    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_queryset(self):
        """
        This view should return a list of all the USERS of particular session.
        """
        session_id = self.kwargs['session_id']
        status = self.kwargs['status']
        print status
        print session_id
        if status == 'present':
            return User.objects.get_present_user(session_id, status)
        else:
            return User.objects.get_absent_user(session_id, status)


class MentorUserDetail(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        This view should return a list of all the sabha as determined by the sabhatype portion of the URL.
        """
        mentor_id = self.kwargs['mentor_id']
        return Profile.objects.mentor(mentor_id)
