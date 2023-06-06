from dataclasses import field
from django.core import serializers
from rest_framework import serializers
from .models import server_user,server_banned,user_slang_count_date,user_sentence,user_slang_count_week,slang_dict

class ServerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = server_user
        fields='__all__'

class ServerSlangSerializer(serializers.ModelSerializer):

    class Meta:
        model = slang_dict
        fields='__all__'
        
class ServerBanSerializer(serializers.ModelSerializer):

    class Meta:
        model = server_banned
        fields='__all__'
        
class UserCountDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_slang_count_date
        fields='__all__'

class UserCountWeekSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_slang_count_week
        fields='__all__'

class UserSentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_sentence
        fields='__all__'