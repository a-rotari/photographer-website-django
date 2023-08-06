# Generated by Django 4.2.1 on 2023-08-03 12:19

from django.db import migrations, models
import django.db.models.deletion
import galleries.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0004_gallery_displayed_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive_url', models.FileField(upload_to=galleries.helpers.get_gallery_archive_upload_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.SlugField(blank=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='galleries.gallery')),
            ],
        ),
    ]