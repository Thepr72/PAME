# Generated by Django 4.0.4 on 2022-05-13 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('grupo', models.IntegerField()),
                ('titulo', models.CharField(max_length=256)),
                ('contenf', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Calificaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alumno', models.IntegerField()),
                ('actividad', models.IntegerField()),
                ('calificacion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]
