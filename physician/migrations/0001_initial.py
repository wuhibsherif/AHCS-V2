# Generated by Django 3.1.6 on 2021-08-12 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_date', models.DateTimeField()),
                ('approved_on_date', models.DateTimeField(null=True)),
                ('health_problem_identified_in_detail', models.TextField(null=True)),
                ('identified_disease_type', models.CharField(max_length=50, null=True)),
                ('action_taken', models.CharField(max_length=50, null=True)),
                ('reason_for_referral', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('feedback', models.TextField(null=True)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referral_approved_by', to='accounts.staff')),
                ('feedback_given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback_given_by', to='accounts.staff')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('referred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to='accounts.staff')),
                ('referred_to_hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referred_to_hospital', to='accounts.hospital')),
                ('referring_hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referring_hospital', to='accounts.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='PatientWaitingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_by', to='accounts.staff')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('physician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_date', models.DateTimeField()),
                ('appointment_date', models.DateTimeField(null=True)),
                ('case', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.hospital')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patient')),
                ('physician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
            ],
        ),
    ]
