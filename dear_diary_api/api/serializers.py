from rest_framework import serializers
from main.models import userLogin
from main.models import MasterTable

class userLoginSerializer (serializers.ModelSerializer):
    class Meta:
        model=userLogin
        fields='__all__'
        
class MasterTableSerializer (serializers.ModelSerializer):
    class Meta:
        model=MasterTable
        fields='__all__'
