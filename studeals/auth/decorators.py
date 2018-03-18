from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def guest(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
