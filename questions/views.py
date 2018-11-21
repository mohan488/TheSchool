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
            messages.success(request, 'Teacher added Successfully')
            return redirect('questions:listteachers')
    else:
        user_form = userForm()
    return render(request, 'questions/registration.html', {'user_form': user_form})

def userLogin(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_principal or user.is_teacher or user.is_student:
                    login(request, user)
                    return redirect('questions:home')
            else:
                messages.error(request, 'User Name or Password is incorrect')
                return render(request, 'questions/login.html')
    else:
        form = loginForm()
    return render(request, 'questions/login.html', {'form': form})

def logout_view(request):
    logout(request)

@login_required
def userProfile(request):
    return render(request, 'questions/user_profile.html')

@login_required
def createQuestion(request):

    if request.method == 'POST':
        form = questionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.teacher = User.objects.get(id=request.user.id)
            question.save()
            messages.success(request, 'Question added Successfully')
            return redirect('questions:listquestions')
    else:
        form = questionForm()
    return render(request, 'questions/question_add.html', {'form': form})


@login_required
def listQuestions(request):
    questions = Question.objects.all()

    return render(request, 'questions/questions_list.html', {'questions': questions})

@login_required
def listStudents(request):
    students = User.objects.filter(is_student=True)

    return render(request, 'questions/students_list.html', {'students': students})

@login_required
def listTeachers(request):
    teachers = User.objects.filter(is_teacher=True)

    return render(request, 'questions/teachers_list.html', {'teachers': teachers})