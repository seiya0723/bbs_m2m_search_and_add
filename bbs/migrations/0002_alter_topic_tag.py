# Generated by Django 3.2.10 on 2022-10-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='tag',
            field=models.ManyToManyField(blank=True, to='bbs.Tag', verbose_name='タグ'),
        ),
    ]
