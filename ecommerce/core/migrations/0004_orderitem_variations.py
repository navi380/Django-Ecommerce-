# Generated by Django 3.0.6 on 2020-05-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='core.Variation'),
        ),
    ]
