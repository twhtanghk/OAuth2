from django.conf import settings
from django import forms
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import int_to_base36
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives

class UserDelete(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined')
        
    def __init__(self, *args, **kwargs):
        super(UserDelete, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = ''
        self.fields['email'].label = 'E-mail'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['date_joined'].label = 'Date Joined'
        self.fields['date_joined'].widget.attrs['readonly'] = True
        
class PasswordResetForm(BasePasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                'serverurl': settings.SERVERURL
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            msg = EmailMultiAlternatives(subject,
                                     email,
                                     from_email,
                                     [user.email])
            msg.attach_alternative(email, "text/html")
            msg.send()
