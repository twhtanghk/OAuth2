from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.static import serve
from registration.forms import RegistrationFormUniqueEmail
from rest_framework.routers import SimpleRouter, Route
from accounts import views
from accounts import forms
from oauth2.views import TokenView
from registration.backends.hmac.views import RegistrationView
from django.contrib import admin

class UserAPIRouter(SimpleRouter):
    def __init__(self, trailing_slash=True):
        super(UserAPIRouter, self).__init__(trailing_slash)
        
router = UserAPIRouter()
router.register(r'api/users', views.UserViewSet, 'user')

urlpatterns = (
    # API
    url(r'^api/users/me/$', views.UserMe.as_view(), name='user-me'),
    url(r'^', include(router.urls)),
    url(r'^api/oauth2/verify/$', TokenView.as_view(), name='oauth2_verify'),
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # browser interface
    url(r'^$', views.UserReadMe.as_view(), name='index'),
    url(r'^users/me/$', views.UserReadMe.as_view(), name='readMe'),
    url(r'^users/(?P<slug>[^\/]+)/$', views.UserRead.as_view(), name='read'),
    url(r'^users/(?P<slug>[^\/]+)/delete/$', views.UserDelete.as_view(), name='delete'),
    url(r'^accounts/profile/$', views.UserReadMe.as_view(), name='profile'),
    # override reset password view to send html email instead of text mail
    url(r'^accounts/password/reset/$', auth_views.password_reset, {'password_reset_form': forms.PasswordResetForm}, name='password_reset'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # override registration view to send html email instead of text mail
    url(r'^accounts/register/$', views.RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^oauth2/verify/$', TokenView.as_view(), name='oauth2_verify'),    # backward compatible, deprecated
    url(r'^developers/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')), # backward compatible, deprecated
)

urlpatterns += (
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
)
