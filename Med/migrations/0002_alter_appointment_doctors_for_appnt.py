# Generated by Django 4.1.7 on 2023-06-06 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Med', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Doctors_for_appnt',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Doctor', to='Med.doctor_profiles'),
        ),
    ]