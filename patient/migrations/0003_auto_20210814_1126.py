# Generated by Django 3.1.6 on 2021-08-14 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_administeredtreatment_medication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xrayexamination',
            old_name='reported_by',
            new_name='requested_to',
        ),
    ]
