# Generated by Django 3.0.8 on 2020-07-09 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('date_add', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('string_id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(default=None, max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('realname', models.CharField(blank=True, max_length=30)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=200)),
                ('profile_img', models.ImageField(upload_to='')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_followers', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('marks', models.ManyToManyField(blank=True, related_name='users', to='GeoAppMain.Mark')),
                ('subscriptions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_subscr', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
