# Generated by Django 3.0.8 on 2021-05-18 16:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('note', models.CharField(help_text='Space to write the order customizations.', max_length=200, verbose_name='note')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='employee.Employee', verbose_name='employee')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='menu.Menu', verbose_name='menu')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='menu.Dish', verbose_name='dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='order.Order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order detail',
                'verbose_name_plural': 'order details',
            },
        ),
    ]
