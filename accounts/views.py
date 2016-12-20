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
from rest_framework import filters, permissions

class UserViewSet(viewsets.ModelViewSet):
    """
    User view for list/create/retrieve/readMe/update/delete of user account in JSON format only
    
    list:    for authenticated user
    create:  deny to create user via api, use web interface only
    retrieve:for authenticated user
    readMe:  for authenticated user
    update:  for authenticated user and owner only
    delete:  deny to delete user via api, use web interface only
    """
    model = User
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_value_regex = '[^/]*'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    ordering = ('username',)
    
    def create(self, request, *args, **kwargs):
        raise PermissionDenied
    
    def readMe(self, request, *args, **kwargs):
        kwargs[self.lookup_field] = request.user.username
        self.kwargs[self.lookup_field] = request.user.username
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if kwargs[self.lookup_field] != request.user.username:
            raise PermissionDenied
        return super(UserViewSet, self).update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if kwargs[self.lookup_field] != request.user.username:
            raise PermissionDenied
        return super(UserViewSet, self).delete(request, *args, **kwargs)
    
class UserExists(RetrieveAPIView):
    model = User
    renderer_classes = [JSONRenderer]
    serializer_class = UserExistsSerializer
    lookup_field = 'username'
    permission_classes = ()
    
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
    
class RegistrationView(BaseRegistrationView):
    """
    Revised RegistrationView of django-registration to support html email
    
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
    """
    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username.lower(), email,
                                                                    password, site,
                                                                    False)
        profile = new_user.registrationprofile_set.all()[0]

        self.send_activation_email(site, profile)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
    
    def send_activation_email(self, site, profile):
        user = profile.user
        ctx_dict = {
            'activation_key': profile.activation_key,
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

