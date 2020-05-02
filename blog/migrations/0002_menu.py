# Generated by Django 3.0.3 on 2020-03-23 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('child', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='blog.Menu')),
            ],
        ),
    ]
