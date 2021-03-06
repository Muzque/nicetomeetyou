# Generated by Django 2.1.2 on 2018-11-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_id', models.FloatField(unique=True)),
                ('headline', models.CharField(max_length=30)),
                ('image', models.TextField()),
                ('keywords', models.CharField(default='', max_length=100)),
                ('author', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=30)),
                ('logo', models.TextField()),
                ('context', models.TextField()),
                ('datePublished', models.DateTimeField()),
                ('dateModified', models.DateTimeField()),
            ],
        ),
    ]
