# Generated by Django 5.0 on 2024-01-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_auto_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]
