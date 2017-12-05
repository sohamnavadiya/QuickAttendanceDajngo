import django_tables2 as tables
from django.conf.urls import url
from django.shortcuts import render

from . import views
from .models import Profile
from .views import ProfileRetrieveAPIView, ProfileFollowAPIView, MentorRetrieveAPIView, UserUnderMentorRetrieveAPIView, \
    UserTypeRetrieveAPIView


class SimpleTable(tables.Table):
    class Meta:
        model = Profile


def simple_list(request):
    queryset = Profile.objects.all()
    table = SimpleTable(queryset)
    return render(request, 'simple_list.html', {'table': table})


urlpatterns = [
    url(r'^profiles/(?P<username>\w+)/?$', ProfileRetrieveAPIView.as_view()),
    url(r'^profiles/(?P<username>\w+)/follow/?$', ProfileFollowAPIView.as_view()),

    # update user profile
    url(r'^profile/(?P<pk>[0-9]+)/?$', views.UserProfile.as_view()),

    url(r'^mentor/(?P<mentor_id>[0-9]+)/?$', UserUnderMentorRetrieveAPIView.as_view()),
    url(r'^user/usertype/(?P<user_type_id>[0-9]+)/?$', UserTypeRetrieveAPIView.as_view()),

    url(r'^mentors/?$', MentorRetrieveAPIView.as_view()),

    # example for show data in tabular form using table lib
    url(r'^usertype1/$', simple_list),
    url(r'^usertype/$', views.UserTypeList.as_view()),
    url(r'^usertype/(?P<pk>[0-9]+)/$', views.UserTypeDetail.as_view()),
    url(r'^userlist/$', views.UserList.as_view()),


]
