# Generated by Django 4.1.7 on 2023-03-02 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0004_alter_salesaccount_notes_alter_salesaccount_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesaccount',
            name='delivaryDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تاريخ التوصيل'),
        ),
    ]