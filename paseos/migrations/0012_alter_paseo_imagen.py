# Generated by Django 5.0.6 on 2024-06-21 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paseos', '0011_alter_reserva_comprobantepago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paseo',
            name='imagen',
            field=models.CharField(default='default_value', max_length=500000),
        ),
    ]
