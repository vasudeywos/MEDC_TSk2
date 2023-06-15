from django.urls import path,include,re_path
from . import views


urlpatterns = [
    path('chat/<staff_username>/<patient_username>/', views.room, name='room'),
]
