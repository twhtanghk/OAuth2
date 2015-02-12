from django.conf import settings

def site(request):
    """
    set baseurl of current application (e.g. http://localhost:3000)
    """
    domain = request.get_host()
    return {
        'domain': domain,
        'serverurl': settings.SERVERURL
    }