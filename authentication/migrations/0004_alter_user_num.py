# Generated by Django 3.2.13 on 2022-05-13 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Num',
            field=models.IntegerField(default=72077),
        ),
    ]
