# Generated by Django 5.0 on 2023-12-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LStore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]