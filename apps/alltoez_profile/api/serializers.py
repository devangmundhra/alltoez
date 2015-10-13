from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

from apps.alltoez_profile.models import UserProfile, Child


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User register serializer returns token
    """
    username = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                                  message=_('Email address already registered.'))])
    key = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'key')
        read_only_fields = ('id', )
        write_only_fields = ('password', )

    def get_key(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        """
        return current user instance
        :param validated_data: Serialized valid data.
        :return user instance
        :rtype object
        """
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['email'] = validated_data['username']
        user = super(UserRegisterSerializer, self).create(validated_data)
        return user


class ChildSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ChildSerializer, self).__init__(many=many, *args, **kwargs)

    def get_delete(self, obj):
        return False

    class Meta:
        model = Child
        fields = ('user', 'name', 'gender', 'age', 'pk', 'id')
        read_only_fields = ('user', 'pk', 'id')


class AlltoezProfileSerializer(serializers.ModelSerializer):
    is_complete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('zipcode', 'city', 'state', 'country',
                  'profile_image', 'gender', 'is_complete', 'user', 'pk')
        read_only_fields = ('user', 'pk')

    def get_is_complete(self, obj):
        return obj.profile_complete()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    children = ChildSerializer(many=True, required=False)
    profile = AlltoezProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'pk', 'username', 'first_name', 'last_name', 'email', 'children', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()

        profile = instance.profile

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance


# class VerifyEmail(APIView, ConfirmEmailView):
#
#     permission_classes = (AllowAny,)
#     allowed_methods = ('POST', 'OPTIONS', 'HEAD')
#
#     def get(self, *args, **kwargs):
#         return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def post(self, request, *args, **kwargs):
#         self.kwargs['key'] = self.request.DATA.get('key', '')
#         confirmation = self.get_object()
#         confirmation.confirm(self.request)
#         return Response({'message': 'ok'}, status=status.HTTP_200_OK)
