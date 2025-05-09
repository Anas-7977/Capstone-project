# Generated by Django 3.0.5 on 2025-04-19 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_productgallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManageFilters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('name', models.SlugField(max_length=255, unique=True)),
                ('field_name', models.CharField(max_length=255)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('start_value', models.FloatField(blank=True, null=True)),
                ('end_value', models.FloatField(blank=True, null=True)),
                ('type', models.CharField(choices=[('range', 'Range'), ('boolean', 'Boolean'), ('search', 'Search'), ('ordering', 'Ordering'), ('basic', 'Basic')], default='basic', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
