# Generated by Django 4.1.7 on 2023-06-07 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_theme_company_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='company_id',
        ),
        migrations.AddField(
            model_name='setoftext',
            name='company_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reviews.company'),
            preserve_default=False,
        ),
    ]
