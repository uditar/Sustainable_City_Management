# Generated by Django 2.1.5 on 2019-02-11 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_lat', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
    ]