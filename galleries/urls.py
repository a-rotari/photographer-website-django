from django.urls import path
from . import views

app_name = 'galleries'

urlpatterns = [
    path('personal/',
         views.display_client_area,
         name='client_area'),
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
    path('toggle/',
         views.toggle_buttons,
         name='toggle_buttons'),
    path('delete-local/',
         views.delete_local,
         name='delete_local'),
    path('',
         views.display_gallery,
         name='display_homepage'),
]
