# Generated by Django 3.1.6 on 2021-08-19 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0016_auto_20210819_0353'),
        ('accounts', '0003_staff_num_waiting'),
        ('lab_technician', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrineAnalysisWaitingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_request', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('albumine', models.BooleanField(default=False)),
                ('blood', models.BooleanField(default=False)),
                ('chemo_leukocyte', models.BooleanField(default=False)),
                ('glucose', models.BooleanField(default=False)),
                ('PH', models.BooleanField(default=False)),
                ('nitrate', models.BooleanField(default=False)),
                ('urobilonogen', models.BooleanField(default=False)),
                ('ketone', models.BooleanField(default=False)),
                ('bilirubin', models.BooleanField(default=False)),
                ('specific_gravity', models.BooleanField(default=False)),
                ('microscopy_leukocyte', models.BooleanField(default=False)),
                ('erythrocyte', models.BooleanField(default=False)),
                ('yeast', models.BooleanField(default=False)),
                ('bacteria', models.SmallIntegerField(null=True)),
                ('squamous_epithelial_cell', models.BooleanField(default=False)),
                ('hyaline_cast', models.BooleanField(default=False)),
                ('granular_cast', models.BooleanField(default=False)),
                ('WBC_casts', models.BooleanField(default=False)),
                ('RBC_cast', models.BooleanField(default=False)),
                ('uric_acid', models.BooleanField(default=False)),
                ('calcium_oxalate', models.BooleanField(default=False)),
                ('triple_phosphate', models.BooleanField(default=False)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urine_rqst_requested_by', to='accounts.staff')),
                ('requested_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urine_rqst_requested_to', to='accounts.staff')),
            ],
        ),
        migrations.DeleteModel(
            name='StoolExaminationWaitingList',
        ),
    ]
