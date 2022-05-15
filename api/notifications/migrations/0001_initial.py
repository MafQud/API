# Generated by Django 3.2.13 on 2022-05-15 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('S', 'SUCCESS'), ('I', 'INFO'), ('W', 'WARNING'), ('E', 'ERROR')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('hyper_link', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'db_table': 'notifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
