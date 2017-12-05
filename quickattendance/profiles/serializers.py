from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Profile, UserType


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'middle_name', 'city', 'state', 'contact_no', 'address',
                  'bod', 'bio', 'image', 'mentor_id', 'user_id')
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'


class ProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user_id','first_name','middle_name','last_name')


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'user_type')


class UserSerializerAll(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, fields=('email', 'username'))

    class Meta:
        model = Profile
        fields = ('user_id', 'user', 'first_name', 'last_name', 'middle_name')
