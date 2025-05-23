# Generated by Django 5.2 on 2025-04-15 04:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_account', models.BooleanField(default=False)),
                ('allow_tagging', models.BooleanField(default=True)),
                ('email_notifications', models.BooleanField(default=True)),
                ('push_notifications', models.BooleanField(default=False)),
                ('dark_mode', models.BooleanField(default=True)),
                ('font_size', models.CharField(default='Medium', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
