# Generated by Django 2.0 on 2018-10-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ischool_profiles_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddress',
            name='address_type',
            field=models.CharField(default='Work', max_length=100, verbose_name='Address Type'),
            preserve_default=False,
        ),
    ]