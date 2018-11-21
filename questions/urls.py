from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'questions'

urlpatterns = [

    path('', views.home, name='home'),
    path('studentregistration/', views.registerStudent, name='registerstudent'),
    path('principalregistration/', views.registerPrincipal, name='registerprincipal'),
    path('teacherregistration/', views.registerTeacher, name='registerteacher'),
    path('login/', views.userLogin, name='userlogin'),
    path('userprofile/', views.userProfile, name='userprofile'),
    path('createquestion/', views.createQuestion, name='createquestion'),
    path('questions/', views.listQuestions, name='listquestions'),
    path('students/', views.listStudents, name='liststudents'),
    path('teachers/', views.listTeachers, name='listteachers'),

]
