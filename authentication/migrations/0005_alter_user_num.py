# Generated by Django 3.2.13 on 2022-05-13 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Num',
            field=models.IntegerField(default=72638),
        ),
    ]