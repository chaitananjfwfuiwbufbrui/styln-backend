from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','user_id', 'email', 'user_name', 'state','type_of_account','image','city','latitude','longitude')

class user_setailed_ser(serializers.ModelSerializer):
    class Meta:
        model = User()
        fields = '__all__'
