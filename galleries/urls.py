from django.urls import path
from . import views

app_name = 'galleries'

urlpatterns = [
    path('personal/',
         views.display_user_galleries,
         name='display_user_galleries'),
    path('people/',
         views.display_people_galleries,
         name='display_people_galleries'),
    path('upload/',
         views.upload,
         name='upload'),
    path('gallery/<slug:slug>/',
         views.display_gallery,
         name='display_gallery'),
    path('modify/',
         views.modify_position,
         name='modify_position'),
    path('',
         views.display_gallery,
         name='display_homepage'),
]
