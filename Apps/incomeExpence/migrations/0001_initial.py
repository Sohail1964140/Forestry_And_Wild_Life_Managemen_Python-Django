# Generated by Django 4.2 on 2023-09-10 12:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('slug', models.SlugField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('slug', models.SlugField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoms', to='incomeExpence.incomesource')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='incomeExpence.expensesource')),
            ],
        ),
    ]