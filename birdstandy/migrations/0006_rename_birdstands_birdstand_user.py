# Generated by Django 4.2.1 on 2023-05-30 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birdstandy', '0005_rename_name_birdstand_bird_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='birdstand',
            old_name='birdstands',
            new_name='user',
        ),
    ]