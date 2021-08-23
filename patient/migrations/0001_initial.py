# Generated by Django 3.1.6 on 2021-08-12 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ManyToManyField(to='accounts.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='XrayExamination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examination_requested', models.CharField(max_length=50)),
                ('date_of_request', models.DateTimeField(auto_now_add=True)),
                ('x_ray_image', models.ImageField(null=True, upload_to='')),
                ('x_ray_report', models.TextField(null=True)),
                ('impressions', models.TextField(null=True)),
                ('date_of_report', models.DateTimeField(null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xray_reported_by', to='accounts.staff')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xray_requested_by', to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='VitalSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.SmallIntegerField()),
                ('height', models.SmallIntegerField()),
                ('bmi', models.SmallIntegerField()),
                ('temperature', models.SmallIntegerField()),
                ('systolic_BP', models.CharField(max_length=10)),
                ('diastolic_BP', models.CharField(max_length=10)),
                ('respiratory_rate', models.CharField(max_length=10)),
                ('heart_rate', models.CharField(max_length=10)),
                ('urine_output', models.CharField(max_length=10)),
                ('blood_sugar_R', models.CharField(max_length=10)),
                ('blood_sugar_F', models.CharField(max_length=10)),
                ('taken_date', models.DateTimeField()),
                ('comment', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('taken_at_hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('taken_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='UrineAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_request', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('date_of_report', models.DateTimeField(null=True)),
                ('albumine', models.SmallIntegerField(null=True)),
                ('blood', models.SmallIntegerField(null=True)),
                ('chemo_leukocyte', models.SmallIntegerField(null=True)),
                ('glucose', models.SmallIntegerField(null=True)),
                ('PH', models.SmallIntegerField(null=True)),
                ('nitrate', models.SmallIntegerField(null=True)),
                ('parasites', models.SmallIntegerField(null=True)),
                ('pus_cell', models.SmallIntegerField(null=True)),
                ('red_blood_cell', models.SmallIntegerField(null=True)),
                ('urobilonogen', models.SmallIntegerField(null=True)),
                ('ketone', models.SmallIntegerField(null=True)),
                ('bilirubin', models.SmallIntegerField(null=True)),
                ('specific_gravity', models.SmallIntegerField(null=True)),
                ('microscopy_leukocyte', models.SmallIntegerField(null=True)),
                ('erythrocyte', models.SmallIntegerField(null=True)),
                ('yeast', models.SmallIntegerField(null=True)),
                ('bacteria', models.SmallIntegerField(null=True)),
                ('squamous_epithelial_cell', models.SmallIntegerField(null=True)),
                ('hyaline_cast', models.SmallIntegerField(null=True)),
                ('granular_cas', models.SmallIntegerField(null=True)),
                ('WBC_casts', models.SmallIntegerField(null=True)),
                ('RBC_cast', models.SmallIntegerField(null=True)),
                ('uric_acid', models.SmallIntegerField(null=True)),
                ('calcium_oxalate', models.SmallIntegerField(null=True)),
                ('triple_phosphate', models.SmallIntegerField(null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urine_reported_by', to='accounts.staff')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urine_requested_by', to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='UltraSound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organ_to_be_examined', models.CharField(max_length=50)),
                ('date_of_request', models.DateTimeField(auto_now_add=True)),
                ('ultra_sound_image', models.ImageField(null=True, upload_to='')),
                ('sonographic_report', models.TextField(null=True)),
                ('date_of_report', models.DateTimeField(null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ultrasound_reported_by', to='accounts.staff')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ultrasound_requested_by', to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='StoolExamination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_request', models.DateTimeField()),
                ('status', models.CharField(default='pending', max_length=50)),
                ('parasites', models.CharField(max_length=50, null=True)),
                ('pus_cell', models.CharField(max_length=50, null=True)),
                ('red_blood_cell', models.CharField(max_length=50, null=True)),
                ('yeast_cell', models.CharField(max_length=50, null=True)),
                ('occult_blood_test', models.CharField(max_length=50, null=True)),
                ('h_pylory_stool_ag_test', models.CharField(max_length=50, null=True)),
                ('date_of_report', models.DateTimeField(null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stool_reported_by', to='accounts.staff')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stool_requested_by', to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription_detail', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('prescribed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='PatientForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('filled_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Hematology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinical_history', models.CharField(max_length=150, null=True)),
                ('date_of_request', models.DateTimeField(null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('date_of_report', models.DateTimeField(null=True)),
                ('lab_technician_comment', models.TextField(null=True)),
                ('CBC', models.SmallIntegerField(null=True)),
                ('BE', models.CharField(max_length=50, null=True)),
                ('TWBC', models.CharField(max_length=50, null=True)),
                ('differential', models.CharField(max_length=50, null=True)),
                ('neutrophil', models.SmallIntegerField(null=True)),
                ('lymphocyte', models.SmallIntegerField(null=True)),
                ('eocynophil', models.SmallIntegerField(null=True)),
                ('basophiles', models.SmallIntegerField(null=True)),
                ('monocyt', models.SmallIntegerField(null=True)),
                ('haemoglobin', models.SmallIntegerField(null=True)),
                ('hemo_TCRIT', models.SmallIntegerField(null=True)),
                ('MCV', models.SmallIntegerField(null=True)),
                ('MCH', models.SmallIntegerField(null=True)),
                ('MCHC', models.SmallIntegerField(null=True)),
                ('RBC', models.SmallIntegerField(null=True)),
                ('RBC_morophology', models.SmallIntegerField(null=True)),
                ('platlet_count', models.SmallIntegerField(null=True)),
                ('EST', models.SmallIntegerField(null=True)),
                ('bleeding_time_test', models.CharField(max_length=50, null=True)),
                ('clot_retraction', models.CharField(max_length=50, null=True)),
                ('coagulation_time', models.CharField(max_length=50, null=True)),
                ('prothrombin_time', models.CharField(max_length=50, null=True)),
                ('PTT', models.CharField(max_length=50, null=True)),
                ('FBS_RBS', models.CharField(max_length=50, null=True)),
                ('blood_group', models.CharField(max_length=50, null=True)),
                ('fibrinogen', models.CharField(max_length=50, null=True)),
                ('coombs_test', models.CharField(max_length=50, null=True)),
                ('CD4', models.SmallIntegerField(null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('reported_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hematology_reported_by', to='accounts.staff')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hematology_requested_by', to='accounts.staff')),
            ],
        ),
    ]
