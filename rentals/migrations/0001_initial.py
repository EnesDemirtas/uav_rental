# Generated by Django 5.0.6 on 2024-05-17 19:09

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('uavs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uav', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='uavs.uav')),
            ],
        ),
    ]