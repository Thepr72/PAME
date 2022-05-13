# Generated by Django 4.0.4 on 2022-05-13 02:37

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='Correo')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Apellido(s)')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='administrativo')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Activo')),
                ('is_admin', models.BooleanField(default=False, help_text="Designates whether the user is an admin in the platform. Admin cannot log into the Django's admin site", verbose_name='Administrador')),
                ('Num', models.IntegerField(default=66203)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Administrador'), (1, 'Profesor'), (2, 'Alumno')], default=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
    ]
