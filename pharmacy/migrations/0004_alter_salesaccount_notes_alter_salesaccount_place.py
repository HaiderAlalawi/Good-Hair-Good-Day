# Generated by Django 4.1.3 on 2023-02-25 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_placeaccountname_alter_salesaccount_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesaccount',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='ملاحظات'),
        ),
        migrations.AlterField(
            model_name='salesaccount',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountPlace', to='pharmacy.placeaccountname', verbose_name='العنوان'),
        ),
    ]