from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Photo


@receiver(pre_delete, sender=Photo)
def remove_image_files(sender, instance, **kwargs):
    """
    A signal that removes the image files from the cloud when a Photo instance
    is deleted.
    """
    try:
        instance.image.delete()  # Attempt to remove the main image file
    except Exception as e:
        print(f"An error occurred while deleting main image: {e}")

    try:
        optimized_photos = instance.optimizedphoto_set.all()
        for optimized_photo in optimized_photos:
            optimized_photo.image.delete()  # Attempt to remove all the associated optimized images
    except Exception as e:
        print(f"An error occurred while deleting optimized images: {e}")
