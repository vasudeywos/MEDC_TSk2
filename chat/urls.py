from django.urls import path,include,re_path
from . import views


urlpatterns = [
    re_path(r"^chat/(?P<staff_username>[\w-]+)/(?P<patient_username>[\w-]+)/$", views.room, name="room"),
]
