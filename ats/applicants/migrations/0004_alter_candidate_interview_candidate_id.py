# Generated by Django 4.2.1 on 2023-07-13 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0003_remove_interview_slot_slot_group_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_interview',
            name='candidate_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='applicants.candidate'),
        ),
    ]
