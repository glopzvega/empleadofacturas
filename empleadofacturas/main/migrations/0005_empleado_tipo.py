# Generated by Django 2.2 on 2019-04-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190425_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='tipo',
            field=models.CharField(choices=[('salario', 'Asalariado'), ('horas', 'Por Hora')], default='salario', max_length=255),
            preserve_default=False,
        ),
    ]
