# Generated by Django 4.1.7 on 2023-06-07 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_remove_theme_company_id_setoftext_company_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='reviewtextblock',
            old_name='text_id',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='reviewtextblock',
            old_name='theme_id',
            new_name='theme',
        ),
        migrations.RenameField(
            model_name='setoftext',
            old_name='company_id',
            new_name='company',
        ),
        migrations.RenameField(
            model_name='setoftext',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='company_id',
            new_name='company',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='set_id',
            new_name='set',
        ),
        migrations.RenameField(
            model_name='theme',
            old_name='user_id',
            new_name='user',
        ),
    ]
