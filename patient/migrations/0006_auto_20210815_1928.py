# Generated by Django 3.1.6 on 2021-08-15 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_staff_num_waiting'),
        ('patient', '0005_auto_20210814_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xrayexamination',
            name='requested_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xray_requested_to', to='accounts.staff'),
        ),
    ]
