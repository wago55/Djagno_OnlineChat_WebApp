# Generated by Django 3.2 on 2021-06-29 05:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_channel', '0005_auto_20210620_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroomchannel',
            name='password',
            field=models.CharField(max_length=19, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
    ]
