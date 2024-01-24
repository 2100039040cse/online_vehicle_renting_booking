# Generated by Django 5.0 on 2024-01-07 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_remove_paymentdetails_cancelled_delete_cancellation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CancellationReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('change_of_plans', 'Change of Plans'), ('found_alternative', 'Found Alternative'), ('booking_mistake', 'Booking Mistake'), ('travel_restrictions', 'Travel Restrictions'), ('unforeseen_circumstances', 'Unforeseen Circumstances')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.paymentdetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
