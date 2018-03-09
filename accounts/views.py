from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model,logout
from django.http import JsonResponse
from .models import User

# Create your views here.

def validate_email(request):
    print("VALIDATE EMAIL....")
    username = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

User = get_user_model()
def register_action(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form'  :   form
    }
    print(request.user.is_authenticated())

    if form.is_valid():
        print(form.cleaned_data)

        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        try:
            new = User.objects.create_user(email=email,password=password)
        except Exception as e:
            print(e)
            data = {
                'error_code': 1 ,
                'is_error': e.args
            }
            return JsonResponse(data)

        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)

            data = {
                'is_register': email
            }
            return JsonResponse(data)
        else:
            data = {
                'error_code': 0 ,
                'is_error': "cannot create user"
            }
            return JsonResponse(data)
    else :
        print(form.errors)

        data = {
            'error_code': 3 ,
            'is_error' : form.errors
        }
        return JsonResponse(data)


def login_action(request):
    form = LoginForm(request.POST or None)
    context = {
        'form'  :   form
    }
    print("LOGIN....")

    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request,email=email, password=password)
        if user is not None:

            login(request, user)
            context['form'] = LoginForm()
            data = {
                'is_login': email
            }

            return JsonResponse(data)
        else:
            data = {
                'is_error': "cannot login"
            }
            print(data)
            return JsonResponse(data)
    else :
        data = {
            'is_form_error': form.errors
        }
        print(data)
        return JsonResponse(data)
