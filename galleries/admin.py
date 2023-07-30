from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Gallery, Photo, OptimizedPhoto

# class PhotoAdmin(admin.ModelAdmin):
#     def delete_queryset(self, request, queryset):
#         """Given a queryset, delete it from the database."""
#         for photo in queryset: # delete the images associated with the queryset
#             photo.image.delete()
#         queryset.delete()


# class OptimizedPhotoAdmin(admin.ModelAdmin):
#     def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
#         print('Triggered delete QUERYSET')
#         for photo in queryset: # delete the images associated with the queryset
#             photo.image.delete()
#             print('Gonna delete a photo from a QUERYSET')
#             input()
#         queryset.delete()

admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(OptimizedPhoto)
# admin.site.register(Photo, PhotoAdmin)
# admin.site.register(OptimizedPhoto, OptimizedPhotoAdmin)
