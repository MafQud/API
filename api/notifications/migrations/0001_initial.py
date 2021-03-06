# Generated by Django 3.2.13 on 2022-05-26 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0003_case_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('S', 'SUCCESS'), ('I', 'INFO'), ('W', 'WARNING'), ('E', 'ERROR')], max_length=1)),
                ('action', models.CharField(choices=[('M', 'Matches'), ('P', 'Publish'), ('D', 'Details'), ('N', 'None')], max_length=1)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='cases.case')),
                ('sent_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'db_table': 'notifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
