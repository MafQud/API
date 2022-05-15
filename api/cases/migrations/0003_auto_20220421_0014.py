# Generated by Django 3.2.13 on 2022-04-21 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_alter_location_address'),
        ('cases', '0002_case_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casedetails',
            name='age',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='casedetails',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='casedetails',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
    ]