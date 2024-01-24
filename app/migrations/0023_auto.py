# Generated by Django 5.0 on 2023-12-26 13:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_delete_auto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_id', models.CharField(max_length=20)),
                ('vehicle_number', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='auto_images/')),
                ('vehicle_name', models.CharField(max_length=100)),
                ('rent_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('driver_name', models.CharField(max_length=100)),
                ('driver_contact', models.CharField(max_length=20)),
                ('driver_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('location', models.CharField(max_length=100)),
                ('station', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('terms_conditions', models.TextField()),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='added_autos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
