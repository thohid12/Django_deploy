# Generated by Django 5.1.1 on 2024-09-13 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fblood', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donar_signup_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=60)),
            ],
        ),
        migrations.DeleteModel(
            name='Donar_info',
        ),
    ]
