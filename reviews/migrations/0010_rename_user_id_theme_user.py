# Generated by Django 4.1.7 on 2023-06-03 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_theme_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='user_id',
            new_name='user',
        ),
    ]