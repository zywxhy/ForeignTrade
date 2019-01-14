from rest_framework.serializers import ModelSerializer
from .models import MyUser


class UsersModelSerializer(ModelSerializer):

    class Meta:
        model = MyUser
        fields =  ['id','type','first_name']
