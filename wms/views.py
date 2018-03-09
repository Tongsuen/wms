from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import json
def home_page(request):
    return render(request, 'home_page.html',{})
def term_page(request):
    return render(request, 'term/term.html',{})

def logout_page(request):
    logout(request)
    return render(request, 'home_page.html',{})
