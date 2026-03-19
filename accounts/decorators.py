from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required



def role_required(allowed_roles=[]):
    def decorator(view_func):

        @login_required
        def wrapper(request, *args, **kwargs):

            if request.user.role in allowed_roles: #check if user's role is allowed 
                return view_func(request, *args, **kwargs)
            
            else:
                return HttpResponseForbidden("403 Forbidden - you're not authorized to access this page.")
            
        return wrapper
    
    return decorator    