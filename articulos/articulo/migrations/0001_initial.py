# Generated by Django 3.2.25 on 2024-09-15 19:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('precio_sin_impuestos', models.DecimalField(decimal_places=2, max_digits=10)),
                ('impuesto_aplicable', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
