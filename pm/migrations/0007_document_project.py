# Generated by Django 2.2 on 2019-05-02 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0006_auto_20190502_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pm.Project'),
        ),
    ]
