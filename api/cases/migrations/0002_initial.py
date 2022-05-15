# Generated by Django 3.2.13 on 2022-05-15 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('files', '0001_initial'),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='casephoto',
            name='file',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.file'),
        ),
        migrations.AddField(
            model_name='casematch',
            name='found',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='found_matches', to='cases.case'),
        ),
        migrations.AddField(
            model_name='casematch',
            name='missing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missing_matches', to='cases.case'),
        ),
        migrations.AddField(
            model_name='casedetails',
            name='case',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='cases.case'),
        ),
        migrations.AddField(
            model_name='casedetails',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
        migrations.AddField(
            model_name='case',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='locations.location'),
        ),
        migrations.AddField(
            model_name='case',
            name='thumbnail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.file'),
        ),
    ]