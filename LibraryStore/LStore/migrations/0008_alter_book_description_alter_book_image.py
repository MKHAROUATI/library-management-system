# Generated by Django 4.2 on 2023-12-08 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LStore', '0007_deletedreservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
