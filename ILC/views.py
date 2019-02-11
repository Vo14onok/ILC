from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
# from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.db import models
from .forms import Login
from samsung.models import Incoming, Outcoming


def topbar(request):
    title = "Hi %s" %(request.user)
    return render(request, 'topbar.html', {'title': title})

def login_user(request):
        title = "Hi %s" %(request.user)
        if request.method == 'POST':
            form = Login(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate (username = cd['username'], password = cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "Well done my padavan!")
                        return redirect('/samsung/')
                    else:
                        messages.error(request, "oops something wrong")
                        return redirect('/login/')
                else:
                    messages.error(request, "Неверный пароль или логин!")
                    return redirect('/login/')
        else:
            form = Login()
        context = {'title': title, 'form': form}
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')
