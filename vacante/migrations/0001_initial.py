# Generated by Django 5.1.5 on 2025-05-07 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_vacante', models.CharField(max_length=100)),
                ('id_vacante', models.IntegerField(unique=True)),
                ('descripcion_vacante', models.TextField()),
                ('ciudad_vacante', models.CharField(max_length=100)),
                ('area_vacante', models.CharField(max_length=100)),
                ('salario_vacante', models.IntegerField()),
                ('empresa_vacante', models.CharField(max_length=100)),
                ('imagen', models.ImageField(default='images/default_vacante.png', upload_to='images/')),
            ],
        ),
    ]
