# Generated by Django 3.2.13 on 2022-05-08 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_alter_casedetails_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casematch',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_matches', to='cases.case'),
        ),
        migrations.AlterField(
            model_name='casematch',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_matches', to='cases.case'),
        ),
    ]
