# Generated by Django 4.1.7 on 2023-06-13 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0026_model_model_data_alter_reviewtextblock_textblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='model_data',
            field=models.FileField(null=True, upload_to='models/'),
        ),
    ]