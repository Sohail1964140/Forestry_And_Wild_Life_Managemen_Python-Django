# Generated by Django 4.2 on 2023-09-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_alter_complaints_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='subject',
            field=models.CharField(max_length=30),
        ),
    ]
