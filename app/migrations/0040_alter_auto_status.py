# Generated by Django 5.0 on 2024-01-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_auto_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('In work, Available after some time', 'In work, Available after some time')], default='Available', max_length=100),
        ),
    ]
