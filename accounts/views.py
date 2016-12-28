# Create your views here.
from django.conf import settings
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from accounts.serializers import UserSerializer, UserExistsSerializer
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from guardian.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic.edit import DeleteView
from rest_framework.exceptions import PermissionDenied
from accounts import forms
from django.views.generic.edit import ModelFormMixin
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from registration import signals
from django.template.loader import render_to_string
from registration.models import RegistrationProfile
from django.core.mail import EmailMultiAlternatives
from warnings import warn
from rest_framework.generics import RetrieveAPIView
from rest_framework import filters, permissions, decorators
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from registration.backends.hmac import views
from django.contrib.sites.shortcuts import get_current_site

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    model = User
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.AllowAny,)
    lookup_value_regex = '[^/]*'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    ordering = ('username',)
    
class UserMe(RetrieveAPIView):
    model = User
    renderer_classes = [JSONRenderer]
    serializer_classes = UserSerializer
    lookup_field = 'username'
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        kwargs[self.lookup_field] = request.user.username
        self.kwargs[self.lookup_field] = request.user.username
    
class UserRead(LoginRequiredMixin, DetailView):
    """
    User view to display user details in HTML format only
    """
    model = User
    template_name = 'read.html' 
    slug_field = 'username'
    return_403 = True
        
class UserReadMe(LoginRequiredMixin, RedirectView):
    """
    User view to display current login user details in HTML format only
    """
    def get_redirect_url(self, **kwargs):
        ret = reverse_lazy('read', args=[self.request.user.username])
        return ret
    
class UserDelete(LoginRequiredMixin, ModelFormMixin, DeleteView):
    """
    User view to create user account in HTML format only
    """
    model = User
    slug_field = 'username'
    form_class = forms.UserDelete
    success_url = reverse_lazy('index')
    return_403 = True
    
    def get_context_data(self, **kwargs):
        context = super(UserDelete, self).get_context_data(**kwargs)
        context['form'] = self.get_form(self.get_form_class())
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs['slug']:
            raise PermissionDenied
        return super(UserDelete, self).dispatch(request, *args, **kwargs)
    
class RegistrationView(views.RegistrationView):
    def register(self, form):
        new_user = self.create_inactive_user(form)
        self.send_activation_email(new_user)
        return new_user
    
    def send_activation_email(self, user):
        site = get_current_site(self.request)
        ctx_dict = {
            'activation_key': self.get_activation_key(user),
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
            'email': user.email,
            'serverurl': settings.SERVERURL,
            'domain': self.request.get_host(),
            'protocol': 'https' if self.request.is_secure() else 'http'            
        }

        # Email subject *must not* contain newlines
        subject = ''.join(\
            render_to_string('registration/activation_email_subject.txt',
                             ctx_dict).splitlines())

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        text_content = render_to_string('registration/activation_email.txt',
                                        ctx_dict)
        try:
            html_content = render_to_string('registration/activation_email.html',
                                            ctx_dict)
        except:
            # If any error occurs during html preperation do not add html content
            # This is here to make sure when we switch from default backend to extended
            # we do not get any missing here
            html_content = None
            # XXX we should not catch all exception for this
            warn('registration/activation_email.html template cannot be rendered. Make sure you have it to send HTML messages. Will send email as TXT')

        msg = EmailMultiAlternatives(subject,
                                     text_content,
                                     from_email,
                                     [to_email])
        if html_content:
            msg.attach_alternative(html_content, "text/html")

        msg.send()

