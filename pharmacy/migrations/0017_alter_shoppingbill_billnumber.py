# Generated by Django 4.1.7 on 2023-07-15 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0016_remove_shoppingbill_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingbill',
            name='billNumber',
            field=models.CharField(blank=True, max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
