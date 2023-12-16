from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Photo, GalleryArchive, Gallery

User = get_user_model()


class GalleryForm(forms.ModelForm):
    slug = forms.SlugField(required=False)
    gallery_type = forms.SlugField(required=False)
    name = forms.CharField(max_length=255)
    displayed_date = forms.DateField(
        required=False, widget=forms.SelectDateWidget)
    description = forms.CharField(widget=forms.Textarea, required=False)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Gallery
        fields = [
            'slug',
            'gallery_type',
            'name',
            'displayed_date',
            'description',
            'users'
        ]

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.all()


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
