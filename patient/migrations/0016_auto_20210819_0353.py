# Generated by Django 3.1.6 on 2021-08-19 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_auto_20210819_0302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hematology',
            old_name='RBC_morophology',
            new_name='RBC_morphology',
        ),
    ]