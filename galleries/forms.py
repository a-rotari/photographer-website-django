from django import forms
from django.forms import ModelForm
from .models import Photo, Gallery


class CreateGalleryForm(forms.Form):
    name = forms.CharField(max_length=255, label='Gallery Name')
    description = forms.Textarea()


class UploadPhotoForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Photo
        fields = '__all__'


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadPhotosForm(forms.Form):
    image = MultipleFileField()
    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())
