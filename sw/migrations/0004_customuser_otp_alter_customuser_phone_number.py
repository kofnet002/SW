# Generated by Django 4.1.6 on 2023-04-14 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sw', '0003_remove_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
