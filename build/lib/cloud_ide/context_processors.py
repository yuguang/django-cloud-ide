from django.conf import settings


def debug(context):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {'DEBUG': settings.DEBUG}

def media(context):
    return {'MEDIA_URL': settings.MEDIA_URL, 'MEDIA_VERSION': settings.MEDIA_VERSION}

def firefox(request):
    firefox = False
    if 'HTTP_USER_AGENT' in request.META:
        index = request.META['HTTP_USER_AGENT'].find('Firefox')
        if index != -1:
            firefox = True
    return {'firefox': firefox}
