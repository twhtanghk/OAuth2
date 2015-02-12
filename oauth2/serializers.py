from rest_framework import serializers
from oauth2_provider.models import AccessToken
from accounts.serializers import UserSerializer
from django.utils import timezone 

class TokenSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField('get_client_id')
    expires_in = serializers.SerializerMethodField('get_expires_in')
    user = UserSerializer()
    
    class Meta:
        model = AccessToken
        fields = ('client_id', 'scope', 'user', 'expires_in')
        
    def get_client_id(self, grant):
        return grant.application.client_id
    
    def get_expires_in(self, grant):
        return (grant.expires - timezone.now()).total_seconds()