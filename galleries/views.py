import os
import uuid
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
from django.views.generic.edit import CreateView
from django.db.models import Max

from PIL import ImageFilter

from .config import optimization_subtypes
from .forms import UploadPhotosForm
from .helpers import get_original_image, image_resize, prepare_galleries, get_people_breadcrumbs, get_gallery_breadcrumbs
from .models import Gallery, OptimizedPhoto, Photo, GalleryPhoto


def display_gallery(request, slug='homepage'):
    try:
        gallery = Gallery.objects.get(slug=slug)
    except Gallery.DoesNotExist:
        if slug == 'homepage':
            gallery = Gallery.objects.create(
                slug='homepage',
                type='homepage',
                name='Maria Rotari Photography',
                description='Photoset for the main page',
            )
            gallery.save()
        else:
            raise Gallery.DoesNotExist
    title = gallery.name
    gallery_photos = gallery.photos.all().order_by('-galleryphoto__photo_position')
    photos_context = []  # create list of photo urls dictionaries for template
    for photo in gallery_photos:
        optimized_photos = photo.optimizedphoto_set.all()
        # dictionary containing subtype '480w' as key and url as value
        photo_data = {
            optimized_photo.image_subtype: optimized_photo.image.url
            for optimized_photo in optimized_photos
        }
        photo_data['position'] = photo.galleryphoto_set.get(gallery=gallery).photo_position
        photo_data['gallery_id'] = gallery.id
        photos_context.append(photo_data)
    if slug == 'homepage':
        template = 'galleries/homepage.html'
    else:
        template = 'galleries/galleries_base.html'
    breadcrumbs = get_gallery_breadcrumbs(gallery)
    return render(request,
                  template,
                  {'title': title, 'breadcrumbs': breadcrumbs, 'photos': photos_context})


def display_people_galleries(request):
    breadcrumbs = get_people_breadcrumbs()
    galleries = Gallery.objects.filter(type='people')
    galleries_data = prepare_galleries(galleries)
    return render(request,
                  'galleries/people_display.html',
                  { 'breadcrumbs': breadcrumbs,
                    'galleries': galleries_data})


def display_user_galleries(request):
    if request.user.is_authenticated:
        galleries = request.user.galleries.all()
        galleries_data = prepare_galleries(galleries)
        return render(
            request, "galleries/people_display.html",
            {"galleries": galleries_data}
        )
    return HttpResponseRedirect(reverse('galleries:display_homepage'))


def modify_position(request):
    if request.user.is_superuser and request.method == 'POST':
        direction = request.POST.get('direction')
        position = int(request.POST.get('position'))
        gallery_id = request.POST.get('gallery_id')
        gallery = Gallery.objects.get(id=gallery_id)
        photo = gallery.photos.get(galleryphoto__photo_position=position)
        if direction == 'up':
            modifier = 1
            compared_photo = gallery.photos.order_by('-galleryphoto__photo_position').first()
        else:
            modifier = -1
            compared_photo = gallery.photos.order_by('-galleryphoto__photo_position').last()
        if photo != compared_photo:
            new_position = position + modifier
            swapped_photo = gallery.photos.get(galleryphoto__photo_position=(new_position))
            updated_position = GalleryPhoto.objects.get(photo=photo, gallery=gallery)
            swapped_position = GalleryPhoto.objects.get(photo=swapped_photo, gallery=gallery)
            updated_position.photo_position = new_position
            swapped_position.photo_position = position
            updated_position.save()
            swapped_position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def upload(request):
    if (not request.user.is_authenticated) or (not request.user.is_staff):
        return HttpResponseRedirect(reverse('galleries:display_homepage'))
    submitted = False
    if request.method == 'POST':
        form = UploadPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data.get('image')  # get the files to upload
            gallery = form.cleaned_data.get('gallery')
            if gallery.photos.all().exists():
                max_position = gallery.photos.aggregate(Max('galleryphoto__photo_position'))
                position = max_position['galleryphoto__photo_position__max']
            else:
                position = 0
            for file in files:
                title = file.name
                # get the file extension of the original image
                ext = os.path.splitext(file.name)[1]
                # generate a new uuid filename with the old extension
                file.name = f'{uuid.uuid4()}{ext}'
                original_image = get_original_image(file)
                # instantiate a Photo object for main photo
                # photo = Photo(image=original_image, title=title)
                photo = Photo(image=None, title=title)
                photo.save()
                position += 1
                # photo.galleries.add(gallery)
                gallery_photo_position = GalleryPhoto(
                    gallery=gallery,
                    photo=photo,
                    photo_position=position
                )
                gallery_photo_position.save()

                for subtype in optimization_subtypes:
                    original_image = get_original_image(file)
                    resized_image = image_resize(
                        original_image, subtype['width'])
                    output_io = BytesIO()
                    # Create the blurred placeholder
                    if subtype['width_suffix'] == 'placeholder':
                        resized_image = resized_image.filter(
                            ImageFilter.BoxBlur(80)
                        )
                    resized_image.save(output_io, format='WEBP')
                    resized_file = InMemoryUploadedFile(
                        output_io,
                        None,
                        name=(
                            os.path.splitext(file.name)[0] +
                            '_' + subtype['width_suffix'] + '.webp'),
                        content_type='image/webp',
                        size=output_io.tell(),
                        charset=None
                    )
                    optimized_photo = OptimizedPhoto(
                        image=resized_file,
                        image_subtype=subtype['width_suffix'],
                        parent_image=photo
                    )
                    optimized_photo.save()
            return HttpResponseRedirect('/upload?submitted=True')
    else:
        form = UploadPhotosForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'galleries/upload.html',
                  {'form': form, 'submitted': submitted, })
