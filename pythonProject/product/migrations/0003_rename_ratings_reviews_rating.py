# Generated by Django 5.0.6 on 2024-05-26 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='ratings',
            new_name='rating',
        ),
    ]
