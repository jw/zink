# Generated by Django 3.2.9 on 2021-12-25 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0004_alter_deployment_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deployment',
            options={'get_latest_by': ['deployment_date'], 'ordering': ['deployment_date']},
        ),
    ]
