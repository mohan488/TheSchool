from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'questions/home.html')

def registerStudent(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_student = True
            user.save()
            return render(request, 'questions/register_done.html', )
    else:
        user_form = userForm()
    return render(request, 'questions/registration.html', {'user_form': user_form})

def registerPrincipal(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        if user_form.is_valid():
            try:
                principal = User.objects.get(is_principal=True)
            except User.DoesNotExist:
                principal = None
            if not principal:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.is_principal = True
                user.save()
                return render(request, 'questions/register_done.html')
            else:
                messages.error(request, 'The School principal already exists please contact administrator')
                return render(request, 'questions/registration.html', {'user_form': user_form})
    else:
        user_form = userForm()
    return render(request, 'questions/registration.html', {'user_form': user_form})

def registerTeacher(request):

    if request.method == 'POST':
        user_form = userForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_teacher = True
            user.save()
            return render(request, 'questions/register_done.html', )
    else:
        user_form = userForm()
    return render(request, 'questions/registration.html', {'user_form': user_form})

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_principal or user.is_teacher or user.is_student:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, 'User Name or Password is incorrect')
                return render(request, 'questions/login.html')
    else:
        form = LoginForm()
    return render(request, 'questions/login.html', {'form': form})

def logout_view(request):
    logout(request)

@login_required
def userProfile(request):
    return render(request, 'questions/user_profile.html')