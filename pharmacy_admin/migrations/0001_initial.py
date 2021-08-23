# Generated by Django 3.1.6 on 2021-08-14 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20210812_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.pharmacy')),
            ],
        ),
    ]
