# Generated by Django 3.2.13 on 2022-05-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_alter_casedetails_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casedetails',
            name='last_seen',
            field=models.DateField(blank=True, null=True),
        ),
    ]
