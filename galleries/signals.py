from django.db.models import Max
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

from .models import Photo, GalleryPhoto


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
            # Attempt to remove all the associated optimized images
            optimized_photo.image.delete()
    except Exception as e:
        print(f"An error occurred while deleting optimized images: {e}")


@receiver(post_delete, sender=GalleryPhoto)
def fill_the_gap(sender, instance, **kwargs):
    """
    Fills the gap in the position values left after deleting GalleryPhoto
    """
    gap_position = instance.photo_position
    gallery = instance.gallery
    max_position = gallery.photos.aggregate(
        Max('galleryphoto__photo_position'))['galleryphoto__photo_position__max']
    print(max_position)
    if (not max_position) or (gap_position == max_position):
        return
    assigned_position = gap_position
    step = 1
    while assigned_position + step <= max_position:
        try:
            gallery_photo = GalleryPhoto.objects.get(
                gallery=gallery, photo_position=(assigned_position + step))
            gallery_photo.photo_position = assigned_position
            gallery_photo.save()
        except:
            step += 1
            continue
        assigned_position += 1
        step = 1
