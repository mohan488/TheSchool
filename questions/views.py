from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.

def home(request):
    return render(request, 'questions/base.html')

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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_principal:
                    login(request, user)
                    response = redirect('/campusHome')
                    return response
                elif user.is_teacher:
                    login(request, user)
                    response = redirect('/CommunityHome')
                    return response
                elif user.is_student:
                    login(request, user)
                    response = redirect('/AdminHome')
                    return response
            else:
                messages.error(request, 'Email or Password is incorrect')
                return redirect('/account/loginPage/')
                #return HttpResponse('Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
