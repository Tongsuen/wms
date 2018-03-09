from accounts.models import User
from rest_framework import serializers
from .models import CarPath

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'name', 'email','password')

class CarPathSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarPath
        fields = ('url', 'name', 'lat','lon','timestamp')
