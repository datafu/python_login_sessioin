# -*- coding: utf-8 -*-  
from django.shortcuts import HttpResponseRedirect
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/online/login/':
            if request.COOKIES.get('is_success','') == '1':
                return HttpResponseRedirect('/online/index/')
            else:
               return None
        
        return None