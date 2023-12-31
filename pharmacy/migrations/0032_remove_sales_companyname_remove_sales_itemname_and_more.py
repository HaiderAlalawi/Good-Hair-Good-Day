# Generated by Django 4.1.7 on 2023-08-18 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0031_newcompanyname_newitemname_newnumberofitem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='companyName',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='itemName',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='salesItem',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='sourceName',
        ),
        migrations.RemoveField(
            model_name='salesaccount',
            name='place',
        ),
        migrations.RemoveField(
            model_name='sourcename',
            name='placeName',
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.newcompanyname'),
        ),
        migrations.DeleteModel(
            name='CompanyName',
        ),
        migrations.DeleteModel(
            name='ItemName',
        ),
        migrations.DeleteModel(
            name='PlaceAccountName',
        ),
        migrations.DeleteModel(
            name='PlaceName',
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
        migrations.DeleteModel(
            name='SalesAccount',
        ),
        migrations.DeleteModel(
            name='SourceName',
        ),
    ]
