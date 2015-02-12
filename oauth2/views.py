# Create your views here.
import re
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from oauth2.serializers import TokenSerializer
from oauth2_provider.models import AccessToken
from django.utils import timezone
from rest_framework.exceptions import ParseError

class TokenView(RetrieveAPIView):
    """
    Token view for retrieve token information in JSON format only
    Please see the details in https://developers.google.com/accounts/docs/OAuth2UserAgent
    
    retrieve: {client_id, scope, user url, expires_in}
    """
    model = AccessToken
    renderer_classes = [JSONRenderer]
    serializer_class = TokenSerializer
    lookup_field = 'token'
    authentication_classes = ()
    permission_classes = ()
    
    def retrieve(self, request, *args, **kwargs):
        bearer = request.META.get('HTTP_AUTHORIZATION', '').strip()
        if bearer is None or bearer == '':
            raise ParseError(detail='invalid_token')
        result = re.match(r'Bearer\s+(?P<token>\w+)', bearer)
        if result is None:
            raise ParseError(detail='invalid_token')
        kwargs[self.lookup_field] = result.groupdict().get(self.lookup_field)
        self.kwargs[self.lookup_field] = kwargs[self.lookup_field]
        token = self.get_object()
        if token.expires < timezone.now():
            raise ParseError(detail='invalid_token')
        return super(TokenView, self).retrieve(request, *args, **kwargs)