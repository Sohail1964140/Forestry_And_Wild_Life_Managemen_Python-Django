# Generated by Django 4.2 on 2023-09-10 12:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offender', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WoodEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='woods', to='core.forestarea')),
                ('offender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='woods', to='offender.offender')),
                ('species', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='woods', to='core.treespecies')),
            ],
        ),
        migrations.CreateModel(
            name='WoodAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='core.customer')),
                ('wood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='wood.woodentry')),
            ],
        ),
        migrations.CreateModel(
            name='TreeAltment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='altments', to='core.forestarea')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='altments', to='core.customer')),
                ('species', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='altments', to='core.treespecies')),
            ],
        ),
    ]