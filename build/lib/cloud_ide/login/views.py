from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('login/login.html', {},
                                  RequestContext(request))

@login_required
def done(request):
    return render_to_response('login/done.html', {'userId': request.user.username}, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


