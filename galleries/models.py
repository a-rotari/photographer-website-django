import os
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Gallery(models.Model):
    """
    Represents a photography gallery.

    A Gallery is a collection of photos and can be one of arbitrary categories,
    e.g. 'personal' or 'nature'. Each gallery may belong to one or more 'users'
    making it accessible from each user's Client Area. Users can download an
    an archive of the  gallery's photos if available.

    Fields:
      - slug: A unique identifier for the gallery.
      - gallery_type: The category to which this gallery belongs.
      - name: The display name of the gallery.
      - displayed_date: Optional date to be displayed alongside the gallery.
      - description: Textual description of the gallery.
      - created_at: Auto-generated timestamp of gallery creation.
      - updated_at: Auto-generated timestamp of last gallery update.
      - photos: Many-to-many relationship with Photo objects.
      - users: Many-to-many relationship with User objects.
    """

    slug = models.SlugField(unique=True, blank=True)
    gallery_type = models.SlugField(blank=True)
    name = models.CharField(max_length=255)
    displayed_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photos = models.ManyToManyField(
        "Photo",
        related_name="galleries",
        blank=True,
        through="GalleryPhoto",
        through_fields=("gallery", "photo"),
    )
    users = models.ManyToManyField(User, related_name="galleries", blank=True)

    def __str__(self):
        return self.name if self.name else 'Unnamed Gallery'

    class Meta:
        verbose_name_plural = "galleries"


class Photo(models.Model):
    """
    Represents a high-quality photograph that can be displayed in a gallery.

    Fields:
      - image: The high-quality image file of the photo.
      - uploaded_at: Auto-generated timestamp of the upload of the photo.
      - title: Optional title for the photo.
      - description: Optional textual description of the photo.
    """
    image = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title if self.title else 'Untitled Photo'


class GalleryPhoto(models.Model):
    """
    Represents the relationship between a Gallery and a Photo.

    Fields:
      - gallery: ForeignKey to the Gallery that contains the photo.
      - photo: ForeignKey to the Photo contained in the Gallery.
      - photo_position: The position of the photo within the gallery.
    """
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    photo_position = models.IntegerField()


class OptimizedPhoto(models.Model):
    """
    Represents an optimized version of a high-quality photograph.
    These optimized photos are used for faster loading based on viewport width.

    Fields:
      - image: The optimized image file.
      - uploaded_at: Auto-generated timestamp of the upload of the photo.
      - image_subtype: A string indicating the photo's intended viewport width.
                       - 'placeholder': lightweight blurred placeholder
                       - '480w': for viewports up to 480px in width
                       - '768w': for viewports of 480+ px in width
                       - '1200w': for viewports of 768+ px in width
                       - '1920w': for viewports of 1200+ px in width
      - parent_image: ForeignKey to the original high-quality Photo.
    """
    image = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_subtype = models.CharField(max_length=20)
    parent_image = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (
            (f"Optimized { self.parent_image.title } " if self.parent_image.title
             else 'Optimized Unnamed Photo ') + self.image_subtype
        )


def get_gallery_archive_upload_path(self, filename):
    filename, ext = os.path.splitext(filename)
    return f"{self.gallery.slug}{ext}"


class GalleryArchive(models.Model):
    """
    Represents an archive of photos associated with a Gallery.

    Fields:
      - gallery: ForeignKey to the Gallery that is archived.
      - archive_url: The URL where the archive can be downloaded.
      - uploaded_at: Auto-generated timestamp of the archive upload.
      - name: The name of the archive.
    """
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    archive_url = models.FileField(upload_to=get_gallery_archive_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.SlugField(blank=True)
