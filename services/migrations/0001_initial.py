# Generated by Django 5.1.3 on 2024-12-17 00:51

import django.db.models.deletion
import services.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='category')),
                ('slug', models.SlugField()),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='tag')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview_text', models.TextField(blank=True, max_length=500)),
                ('preview_video_url', models.URLField(blank=True, null=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to=services.models.get_upload_to)),
                ('price', models.IntegerField(null=True)),
                ('slug', models.SlugField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.category')),
                ('tags', models.ManyToManyField(blank=True, to='services.tag')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('subtitle', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=services.models.get_upload_to)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_section', to='services.service')),
            ],
            options={
                'verbose_name': 'Секция услуги',
                'verbose_name_plural': 'Секции услуги',
                'ordering': ['order'],
            },
        ),
    ]
