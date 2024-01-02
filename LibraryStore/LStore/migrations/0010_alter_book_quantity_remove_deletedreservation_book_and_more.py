# Generated by Django 4.2 on 2023-12-15 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LStore', '0009_alter_book_image_remove_reservation_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='deletedreservation',
            name='book',
        ),
        migrations.AlterField(
            model_name='deletedreservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='deletedreservation',
            name='book',
            field=models.ManyToManyField(to='LStore.book'),
        ),
    ]
