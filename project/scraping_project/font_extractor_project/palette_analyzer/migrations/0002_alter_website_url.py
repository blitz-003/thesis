# Generated by Django 5.0.6 on 2024-05-28 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('palette_analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.URLField(),
        ),
    ]