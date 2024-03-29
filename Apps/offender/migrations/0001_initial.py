# Generated by Django 4.2 on 2023-09-10 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('address', models.TextField(max_length=80)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('fineAmount', models.IntegerField()),
                ('contact', models.CharField(max_length=15)),
            ],
        ),
    ]
