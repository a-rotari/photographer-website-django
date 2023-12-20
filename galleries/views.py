import os
import uuid
from datetime import date, datetime
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Max
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import resolve, reverse
from django.views.generic.edit import CreateView

from appointments.helpers import create_calendar
from appointments.models import Day
from dateutil.relativedelta import relativedelta
from PIL import ImageFilter

from .config import optimization_subtypes
from .forms import ContactForm, UploadPhotosForm, GalleryForm
from .helpers import (get_client_area_breadcrumbs, get_gallery_breadcrumbs,
                      get_original_image, get_people_breadcrumbs, image_resize,
                      prepare_galleries, get_ordered_gallery_photos,
                      ensure_homepage_gallery, prepare_photo_context)
from .models import Gallery, GalleryPhoto, OptimizedPhoto, Photo


def display_homepage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('valid')
            # Process the data in form.cleaned_data
            # For example, send an email or save it to the database
            pass
    else:
        form = ContactForm()

    return render(request, 'galleries/home.html', {'form': form})


def create_gallery(request):
    pass


def manage_galleries(request):
    template = (
        'galleries/manage_galleries.html'
    )
    form = GalleryForm()
    context = {
        'form': form
    }
    return render(request, template, context)


def display_gallery(request: HttpRequest, slug: str = 'homepage') -> HttpResponse:
    """
    Display a gallery page based on the given slug.

    Parameters:
    - request: HttpRequest object
    - slug: slug of the gallery to display, default is 'homepage'

    Returns:
    - HttpResponse with the gallery page
    """
    if slug == 'homepage':
        gallery = ensure_homepage_gallery()
    else:
        gallery = get_object_or_404(Gallery, slug=slug)

    title = gallery.name
    gallery_photos = get_ordered_gallery_photos(gallery)
    photo_context_data = prepare_photo_context(gallery_photos, gallery)

    template = (
        'galleries/homepage.html' if slug == 'homepage'
        else 'galleries/galleries_base.html'
    )
    for p in photo_context_data:
        print(p['position'])
    breadcrumbs = get_gallery_breadcrumbs(gallery)
    context = {
        'title': title,
        'breadcrumbs': breadcrumbs,
        'photos': photo_context_data
    }
    return render(request, template, context)


def display_people_galleries(request):
    breadcrumbs = get_people_breadcrumbs()
    galleries = Gallery.objects.filter(gallery_type='people')
    galleries_data = prepare_galleries(galleries)
    return render(request,
                  'galleries/people_display.html',
                  {'breadcrumbs': breadcrumbs,
                   'galleries': galleries_data})


def display_client_area(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('galleries:display_homepage'))

    today = date.today()
    this_month_name = today.strftime('%B')
    this_month_days, this_month_dummy_days = create_calendar(today)
    appointment_days = Day.objects.filter(client=request.user, date__gte=today)
    next_month_date = today + relativedelta(months=1)
    next_month_name = next_month_date.strftime('%B')
    next_month_days, next_month_dummy_days = create_calendar(next_month_date)

    breadcrumbs = get_client_area_breadcrumbs()

    galleries = request.user.galleries.all()
    galleries_data = prepare_galleries(galleries)
    return render(
        request, "galleries/client_area.html",
        {'breadcrumbs': breadcrumbs,
            'galleries': galleries_data,
            'this_month_name': this_month_name,
            'this_month_days': this_month_days,
            'this_month_dummy_days': this_month_dummy_days,
            'next_month_name': next_month_name,
            'next_month_days': next_month_days,
            'next_month_dummy_days': next_month_dummy_days,
            'appointment_days': appointment_days})


def modify_position(request):
    if request.user.is_superuser and request.method == 'POST':
        direction = request.POST.get('direction')
        position = int(request.POST.get('position'))
        gallery_id = request.POST.get('gallery_id')
        gallery = Gallery.objects.get(id=gallery_id)
        photo = gallery.photos.get(galleryphoto__photo_position=position)
        if direction == 'up':
            modifier = 1
            compared_photo = gallery.photos.order_by(
                '-galleryphoto__photo_position').first()
        else:
            modifier = -1
            compared_photo = gallery.photos.order_by(
                '-galleryphoto__photo_position').last()
        if photo != compared_photo:
            new_position = position + modifier
            swapped_photo = gallery.photos.get(
                galleryphoto__photo_position=(new_position))
            updated_position = GalleryPhoto.objects.get(
                photo=photo, gallery=gallery)
            swapped_position = GalleryPhoto.objects.get(
                photo=swapped_photo, gallery=gallery)
            updated_position.photo_position = new_position
            swapped_position.photo_position = position
            updated_position.save()
            swapped_position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_local(request):
    if request.user.is_superuser and request.method == 'POST':
        position = int(request.POST.get('position'))
        gallery_id = request.POST.get('gallery_id')
        gallery = Gallery.objects.get(id=gallery_id)
        GalleryPhoto.objects.get(
            gallery=gallery, photo_position=position).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_global(request):
    if request.user.is_superuser and request.method == 'POST':
        position = int(request.POST.get('position'))
        gallery_id = request.POST.get('gallery_id')
        gallery = Gallery.objects.get(id=gallery_id)
        photo = GalleryPhoto.objects.get(
            gallery=gallery, photo_position=position).photo
        photo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def toggle_buttons(request):
    if (not request.user.is_authenticated) or (not request.user.is_staff):
        return HttpResponseRedirect(reverse('galleries:display_homepage'))
    if 'toggle_buttons' in request.session:
        request.session['toggle_buttons'] = not request.session['toggle_buttons']
    else:
        request.session['toggle_buttons'] = True
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
                max_position = gallery.photos.aggregate(
                    Max('galleryphoto__photo_position'))
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
