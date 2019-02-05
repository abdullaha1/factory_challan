# Generated by Django 2.1.3 on 2019-02-03 10:35

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallanData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('challan_type_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='master_data.ChallanTypes')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='challandata_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='challandata_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]