import shutil
from io import BytesIO
from django.db.models import QuerySet
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            TemporaryUploadedFile)
from django.urls import reverse
from typing import List, Dict, Union, TYPE_CHECKING

from PIL import Image

from .models import Gallery

HOMEPAGE_SLUG = 'homepage'
HOMEPAGE_TYPE = 'homepage'
HOMEPAGE_NAME = 'Maria Rotari Photography'
HOMEPAGE_DESCRIPTION = 'Photoset for the main page'


def image_resize(image, tgt_width):
    with Image.open(image) as img:
        width, height = img.size
        ratio = width / height
        tgt_height = int(tgt_width / ratio)
        img = img.resize((tgt_width, tgt_height), Image.ANTIALIAS)
        return img


def copy_in_memory_uploaded_file(file):
    file_name = file.name
    file_size = file.size
    content_type = file.content_type
    charset = file.charset
    field_name = file.field_name
    content_type_extra = file.content_type_extra

    copied_file = InMemoryUploadedFile(
        file=None,
        field_name=field_name,
        name=file_name,
        content_type=content_type,
        size=file_size,
        charset=charset,
        content_type_extra=content_type_extra,
    )

    copied_bytesio = BytesIO()
    original_bytesio = file.file
    original_position = original_bytesio.tell()
    original_bytesio.seek(0)
    copied_bytesio.write(original_bytesio.getvalue())
    original_bytesio.seek(original_position)
    copied_file.file = copied_bytesio
    return copied_file


def copy_temporary_uploaded_file(file):
    copied_file = TemporaryUploadedFile(
        name=file.name,
        size=file.size,
        content_type=file.content_type,
        charset=file.charset,
        content_type_extra=file.content_type_extra,
    )
    shutil.copyfile(file.temporary_file_path(),
                    copied_file.temporary_file_path())
    copied_file.seek(0)
    return copied_file


def get_original_image(file):
    if isinstance(file, InMemoryUploadedFile):
        return copy_in_memory_uploaded_file(file)
    else:
        return copy_temporary_uploaded_file(file)


def prepare_galleries(galleries):
    galleries_data = []
    for gallery in galleries:
        thumbnail_url = (
            gallery.photos.first()
            .optimizedphoto_set.get(image_subtype="480w")
            .image.url
        )
        gallery_archive = gallery.galleryarchive_set.first()
        archive_url = gallery_archive.archive_url.url if gallery_archive else ""

        gallery_data = {
            "thumbnail": thumbnail_url,
            "slug": gallery.slug,
            "title": gallery.name,
            "displayed_date": gallery.displayed_date,
            "archive_url": archive_url,
        }
        galleries_data.append(gallery_data)
    return galleries_data


def prepare_breadcrumbs(*args):
    breadcrumbs = []
    for breadcrumb in args:
        breadcrumbs.append(breadcrumb)
    return breadcrumbs


def get_gallery_breadcrumbs(gallery):
    home = {"text": "Home", "href": reverse("galleries:display_homepage")}
    current_gallery = {"text": gallery.name, "href": ""}

    if gallery.gallery_type == "people":
        people = {
            "text": "People",
            "href": reverse("galleries:display_people_galleries"),
        }
        return prepare_breadcrumbs(home, people, current_gallery)
    elif gallery.gallery_type == "urban" or gallery.gallery_type == "nature":
        return prepare_breadcrumbs(home, current_gallery)
    elif gallery.gallery_type == "personal":
        personal_dashboard = {
            "text": "Client Area",
            "href": reverse("galleries:client_area"),
        }
        return prepare_breadcrumbs(home, personal_dashboard, current_gallery)
    return []


def get_people_breadcrumbs():
    home = {"text": "Home", "href": reverse("galleries:display_homepage")}
    people = {"text": "People", "href": ""}
    breadcrumbs = prepare_breadcrumbs(home, people)
    return breadcrumbs


def get_client_area_breadcrumbs():
    home = {"text": "Home", "href": reverse("galleries:display_homepage")}
    client_area = {"text": "Client Area", "href": ""}
    breadcrumbs = prepare_breadcrumbs(home, client_area)
    return breadcrumbs


def get_ordered_gallery_photos(gallery: Gallery) -> QuerySet:
    """
    Returns photos for a given gallery ordered by their position.
    """
    return gallery.photos.all().order_by('-galleryphoto__photo_position')


def ensure_homepage_gallery() -> Gallery:
    """
    Ensures that a homepage gallery exists, creates one if not, and returns it.
    """
    gallery, created = Gallery.objects.get_or_create(
        slug=HOMEPAGE_SLUG,
        defaults={
            'type': HOMEPAGE_TYPE,
            'name': HOMEPAGE_NAME,
            'description': HOMEPAGE_DESCRIPTION,
        }
    )
    return gallery


def prepare_photo_context(gallery_photos: QuerySet, gallery: Gallery) -> List[Dict[str, Union[str, int]]]:
    """
    Prepares the context data for photos in a gallery.
    """
    photo_context_data = []
    for photo in gallery_photos:
        optimized_photos = photo.optimizedphoto_set.all()
        photo_data = {
            optimized_photo.image_subtype: optimized_photo.image.url
            for optimized_photo in optimized_photos
        }
        photo_data.update({
            'position': photo.galleryphoto_set.get(gallery=gallery).photo_position,
            'gallery_id': gallery.id
        })
        photo_context_data.append(photo_data)
    return photo_context_data
