# Generated by Django 3.2.5 on 2021-07-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generated_csv',
            name='path',
            field=models.FileField(blank=True, null=True, upload_to='static/files/'),
        ),
    ]
