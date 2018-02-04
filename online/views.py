# -*- coding: utf-8 -*-
"""
requests.api
~~~~~~~~~~~~

This module implements the Requests API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: Apache2, see LICENSE for more details.
"""
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django import forms
from online.models import User

# Create your views here.
class UserForm(forms.Form):
    r"""
    表单
    """
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())


def regist(req):
    r"""
    #注册
    """
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            User.objects.create(username= username,password=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
        c=csrf(req)
        c.update({'uf':uf})
    return render_to_response('login.html',context=c)#或者render版本的
    
def login(req):
    if  req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                #is_success 1 成功 直接跳转到登录页面
                response.set_cookie('is_success','1')
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/online/login/')
    else:
        uf = UserForm()
        c=csrf(req)
        c.update({'uf':uf})
    return render_to_response('login.html',context=c)#或者
   
def index(req):
    r"""
    #登陆成功
    """
    username = req.COOKIES.get('username','')
    return render_to_response('index.html' ,{'username':username})


def logout(req):
    r"""
    #退出
    """
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    response.set_cookie('is_success','0')
    return response