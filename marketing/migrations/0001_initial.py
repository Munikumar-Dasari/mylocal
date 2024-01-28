# Generated by Django 4.2 on 2024-01-20 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import marketing.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinystoreapp', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blog_name', models.CharField(max_length=100)),
                ('Image1', models.ImageField(blank=True, upload_to=marketing.models.path_and_rename_blog)),
                ('Image2', models.ImageField(blank=True, upload_to=marketing.models.path_and_rename_blog)),
                ('description1', models.TextField(max_length=5000)),
                ('description2', models.TextField(max_length=5000)),
                ('description3', models.TextField(blank=True, default='True', max_length=5000, null=True)),
                ('description4', models.TextField(blank=True, default='True', max_length=5000, null=True)),
                ('heading1', models.TextField(max_length=200)),
                ('heading2', models.TextField(max_length=200)),
                ('heading3', models.TextField(blank=True, default='True', max_length=200, null=True)),
                ('heading4', models.TextField(blank=True, default='True', max_length=200, null=True)),
                ('timestamp_field', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'blog',
                'ordering': ['-timestamp_field'],
            },
        ),
        migrations.CreateModel(
            name='MarketingRegister',
            fields=[
                ('marketing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=45)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.CharField(max_length=100)),
                ('profile_image', models.ImageField(default='marketing/blank_profile.webp', null=True, upload_to=marketing.models.rename_marketing)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Marketing_register',
            },
        ),
        migrations.CreateModel(
            name='Privacy1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5000)),
                ('Heading', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('timestamp_field', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'privacy',
                'ordering': ['timestamp_field'],
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=5000)),
                ('Heading', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('timestamp_field', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'terms',
                'ordering': ['timestamp_field'],
            },
        ),
    ]
