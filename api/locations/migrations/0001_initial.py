# Generated by Django 3.2.13 on 2022-04-19 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ar', models.CharField(max_length=64)),
                ('name_en', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Governorate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ar', models.CharField(max_length=64)),
                ('name_en', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'governorate',
                'verbose_name_plural': 'governorates',
                'db_table': 'governorates',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.city')),
                ('gov', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.governorate')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'db_table': 'locations',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='gov',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='locations.governorate'),
        ),
    ]
