# Generated by Django 2.2 on 2019-05-01 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0003_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='formation',
            name='departement',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='pm.Departement'),
            preserve_default=False,
        ),
    ]
