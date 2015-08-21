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
                                                                 message=_('Username Already exists.'))])
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password','token')
        read_only_fields = ('id', )
        write_only_fields = ('password', )

    def get_token(self, obj):
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

class UserAccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name')


class UpdateUserSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = UserProfile
        fields = ('gender', 'zipcode', 'city', 'state', 'user')

    def update(self, instance, validated_data):
        user_details = validated_data.pop('user')
        user = self.context['request'].user
        user.first_name = user_details.get('first_name')
        user.last_name = user_details.get('last_name')
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class ChildSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ChildSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Child
        fields = ('user', 'name', 'gender', 'age', )
        read_only_fields = ('user', )


class AlltoezProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name',)


class UserInternalSerializer(serializers.HyperlinkedModelSerializer):
    children = ChildSerializer(many=True, required=False)
    profile = AlltoezProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'pk', 'username', 'first_name', 'last_name', 'email', 'children', 'profile')

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
