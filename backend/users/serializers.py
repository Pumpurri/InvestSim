from rest_framework import serializers
from .models import CustomUser  
from stocks.models import Stock 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
    