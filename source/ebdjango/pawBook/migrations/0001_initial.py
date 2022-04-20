# Generated by Django 4.0.3 on 2022-04-16 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usern', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WeatherPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usern', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=40)),
            ],
        ),
    ]
