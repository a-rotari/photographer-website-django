from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('login/',
         views.login_and_create_appointment,
         name='login_and_create_appointment'),
    path('',
         views.create_appointment,
         name='create_appointment'),
]
