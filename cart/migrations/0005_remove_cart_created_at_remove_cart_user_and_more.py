# Generated by Django 5.0.7 on 2024-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_session_id_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.AlterField(
            model_name='cart',
            name='session_id',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
