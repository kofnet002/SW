# Generated by Django 4.1.6 on 2023-04-19 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
