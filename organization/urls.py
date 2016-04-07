from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from registration.forms import RegistrationFormUniqueEmail
from rest_framework.routers import SimpleRouter, Route
from accounts import views
from accounts import forms
from oauth2.views import TokenView

class UserAPIRouter(SimpleRouter):
    def __init__(self, trailing_slash=True):
        super(UserAPIRouter, self).__init__(trailing_slash)
        self.routes.insert(0,
            Route(
                url=r'^{prefix}/me{trailing_slash}$',
                mapping={
                    'get': 'readMe',
                },
                name='{basename}-me',
                initkwargs={'suffix': 'Me'}
            )
        )
        
router = UserAPIRouter()
router.register(r'api/users', views.UserViewSet)

urlpatterns = patterns('',
    # API
    url(r'^', include(router.urls)),
    url(r'^api/oauth2/verify/$', TokenView.as_view(), name='oauth2_verify'),
    url(r'^api/users/(?P<username>[^\/]+)/exists/$', views.UserExists.as_view(), name='exists'),
    # browser interface
    url(r'^$', views.UserReadMe.as_view(), name='index'),
    url(r'^users/me/$', views.UserReadMe.as_view(), name='readMe'),
    url(r'^users/(?P<slug>[^\/]+)/$', views.UserRead.as_view(), name='read'),
    url(r'^users/(?P<slug>[^\/]+)/delete/$', views.UserDelete.as_view(), name='delete'),
    url(r'^accounts/profile/$', views.UserReadMe.as_view(), name='profile'),
    # override reset password view to send html email instead of text mail
    url(r'^accounts/password/reset/$', auth_views.password_reset, {'password_reset_form': forms.PasswordResetForm}, name='auth_password_reset'),
    # override registration view to send html email instead of text mail
    url(r'^accounts/register/$', views.RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^oauth2/verify/$', TokenView.as_view(), name='oauth2_verify'),    # backward compatible, deprecated
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')), # backward compatible, deprecated
    url(r'^developers/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)

urlpatterns += patterns(
    '',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)