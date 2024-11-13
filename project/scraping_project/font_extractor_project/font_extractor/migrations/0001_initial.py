# Generated by Django 5.0.6 on 2024-05-27 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FontSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_size', models.CharField(max_length=50)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='font_extractor.website')),
            ],
        ),
    ]
