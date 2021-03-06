# Generated by Django 2.2 on 2019-05-02 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0005_auto_20190501_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='departement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pm.Departement'),
        ),
        migrations.AlterField(
            model_name='message',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pm.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pm.DossierEmploye'),
        ),
    ]
