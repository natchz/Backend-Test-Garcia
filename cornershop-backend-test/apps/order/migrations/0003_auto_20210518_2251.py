# Generated by Django 3.0.8 on 2021-05-18 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('order', '0002_auto_20210518_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(to='menu.Dish', verbose_name='dishes'),
        ),
        migrations.DeleteModel(
            name='ChosenDish',
        ),
    ]