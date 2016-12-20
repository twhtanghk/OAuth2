from django.conf import settings
from rest_framework import serializers
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name')
        
    def get_url(self, user):
        return settings.SERVERURL + str(reverse_lazy('user-detail', args=[user.username]))
    
class UserExistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
