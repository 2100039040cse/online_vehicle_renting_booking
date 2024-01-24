# Generated by Django 5.0 on 2024-01-02 16:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_alter_auto_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdetails',
            name='ride_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='auto',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='auto',
            name='status',
            field=models.CharField(default='Available', max_length=100),
        ),
    ]
