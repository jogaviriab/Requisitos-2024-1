# Generated by Django 5.0.6 on 2024-06-21 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paseos', '0009_alter_paseo_imagen_alter_reserva_comprobantepago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paseo',
            name='imagen',
            field=models.CharField(default='default_value', max_length=15000),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='comprobantePago',
            field=models.CharField(default='default_value', max_length=5000),
        ),
    ]
