# Generated by Django 4.1.7 on 2023-03-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deployment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deployment",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
