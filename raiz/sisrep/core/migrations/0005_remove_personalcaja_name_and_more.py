# Generated by Django 5.0.2 on 2024-08-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_personalcaja_delete_venta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalcaja',
            name='name',
        ),
        migrations.RemoveField(
            model_name='personalcaja',
            name='other_field1',
        ),
        migrations.RemoveField(
            model_name='personalcaja',
            name='other_field2',
        ),
        migrations.AddField(
            model_name='personalcaja',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='personalcaja',
            name='nombre_usuario_perseo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='personalcaja',
            name='sucursal',
            field=models.CharField(blank=True, choices=[('JACALA', 'JACALA'), ('ACAXOCHITLAN', 'ACAXOCHITLAN'), ('TENANGO DE DORIA', 'TENANGO DE DORIA'), ('EL CEREZO', 'EL CEREZO'), ('SAN AGUSTIN TLAXIACA', 'SAN AGUSTIN TLAXIACA'), ('SAN JOSE TEPENENE', 'SAN JOSE TEPENENE'), ('ACTOPAN CIMA', 'ACTOPAN CIMA'), ('ACTOPAN OCAMPO', 'ACTOPAN OCAMPO'), ('ACTOPAN TUZO', 'ACTOPAN TUZO'), ('PROGRESO DE OBREGON', 'PROGRESO DE OBREGON'), ('MIXQUIAHUALA', 'MIXQUIAHUALA'), ('TUZO MIXQUIAHUALA', 'TUZO MIXQUIAHUALA'), ('TLAHUELILPAN', 'TLAHUELILPAN'), ('APAXCO AZUL', 'APAXCO AZUL'), ('TEXQUISQUIAC', 'TEXQUISQUIAC')], max_length=50, null=True),
        ),
    ]
