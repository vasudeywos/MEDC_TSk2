from django.urls import path,include
from . import views
from users.views import Home,PatientProf,StaffProf,StaffSignUpView,profile

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('accounts2/', include('django.contrib.auth.urls')),
    path('patient/google-login/', views.patient_google_login, name='patient_google_login'),
    path('patient/profile/', PatientProf.as_view(), name='patient_pg'),
    path('staff/profile/', StaffProf.as_view(), name='staff_pg'),
    path('accounts2/', include('django.contrib.auth.urls')),
    path('accounts2/signup/staff/', StaffSignUpView.as_view(), name='staff_signup'),
    path('profile/', profile, name='profile'),
    path('login2/', views.custom_login, name='login2'),
    path('patienttablelist/', views.PatientTablist, name='patienttablist'),
]
