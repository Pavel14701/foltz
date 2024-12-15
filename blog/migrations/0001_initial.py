# Generated by Django 5.1.3 on 2024-12-15 09:52

import blog.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview_text', models.TextField(blank=True, max_length=500)),
                ('preview_video_url', models.URLField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=200, unique=True)),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to=blog.models.get_upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=blog.models.get_upload_to)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_section', to='blog.blog')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
