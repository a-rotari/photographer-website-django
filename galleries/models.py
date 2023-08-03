from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class Gallery(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    type = models.SlugField(blank=True)
    name = models.CharField(max_length=255)
    displayed_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photos = models.ManyToManyField('Photo', related_name='galleries', blank=True, through='GalleryPhoto', through_fields=('gallery', 'photo'))
    users = models.ManyToManyField(User, related_name='galleries', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "galleries"


class Photo(models.Model):
    image = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    photo_position = models.IntegerField()


@receiver(pre_delete, sender=Photo) # a signal that removes the image files from the cloud when Photo instance is deleted
def remove_image_files(sender, instance, **kwargs):
    instance.image.delete()         # the main image file is removed
    optimized_photos = instance.optimizedphoto_set.all()
    for optimized_photo in optimized_photos:
        optimized_photo.image.delete()      # and all the associated optimized images are removed


class OptimizedPhoto(models.Model):
    image = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_subtype = models.CharField(max_length=20)
    parent_image = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
    )
