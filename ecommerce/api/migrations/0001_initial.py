# Generated by Django 4.2.7 on 2023-11-10 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('postcode', models.CharField(max_length=32)),
                ('street', models.CharField(max_length=128)),
                ('building_number', models.CharField(max_length=32)),
                ('apartament_number', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default=None, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='./images')),
                ('thumbnail', models.ImageField(upload_to='./thumbnails')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_products_summary', models.JSONField()),
                ('order_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('price', models.FloatField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.address')),
            ],
        ),
    ]