# Generated by Django 5.2.3 on 2025-06-28 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ldr_left_top', models.IntegerField()),
                ('ldr_right_top', models.IntegerField()),
                ('ldr_left_bottom', models.IntegerField()),
                ('ldr_right_bottom', models.IntegerField()),
                ('solar_value', models.IntegerField()),
            ],
        ),
    ]
