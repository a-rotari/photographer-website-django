from PIL import Image
from io import BytesIO
import shutil

from django.urls import reverse
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile


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
        content_type_extra=content_type_extra
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
    shutil.copyfile(
        file.temporary_file_path(),
        copied_file.temporary_file_path()
    )
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
            .optimizedphoto_set.get(image_subtype='480w')
            .image.url
        )
        gallery_data = {
            'thumbnail': thumbnail_url,
            'slug': gallery.slug,
            'title': gallery.name
        }
        galleries_data.append(gallery_data)
    return galleries_data

def prepare_breadcrumbs(*args):
    breadcrumbs = []
    for breadcrumb in args:
        breadcrumbs.append(breadcrumb)
    return breadcrumbs



def get_gallery_breadcrumbs(gallery):
    home = { 'text': 'Home',
             'href': reverse('galleries:display_homepage')}
    current_gallery = { 'text': gallery.name,
                        'href': '#'}

    if gallery.type == 'people':
        people = { 'text': 'People',
                    'href': reverse('galleries:display_people_galleries')}
        return prepare_breadcrumbs(home, people, current_gallery)
    elif gallery.type == 'urban' or gallery.type == 'nature':
        return prepare_breadcrumbs(home, current_gallery)
    elif gallery.type == 'personal':
        personal_dashboard = { 'text': 'Personal Dashboard',
                               'href': reverse('galleries:display_user_galleries')}
        return prepare_breadcrumbs(home, personal_dashboard, current_gallery)
    return []


def get_people_breadcrumbs():
    home = { 'text': 'Home',
             'href': reverse('galleries:display_homepage')}
    people = { 'text': 'People',
              'href': '#'}
    breadcrumbs = prepare_breadcrumbs(home, people)
    return breadcrumbs
