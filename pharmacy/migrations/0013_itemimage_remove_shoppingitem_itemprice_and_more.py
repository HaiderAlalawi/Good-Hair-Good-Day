# Generated by Django 4.1.7 on 2023-07-15 20:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0012_remove_shoppingbill_shoppingitem_shoppingitem_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images\\item')),
            ],
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='ItemPrice',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='companyName',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='description',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='itemName',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='numberOfItem',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='sourceName',
        ),
        migrations.RemoveField(
            model_name='shoppingitem',
            name='unitPrice',
        ),
        migrations.AlterField(
            model_name='customerinformation',
            name='phoneNumber',
            field=models.CharField(max_length=50, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='shoppingitem',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='الرمز التسلسلي')),
                ('size', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='الوصف')),
                ('unitPrice', models.IntegerField(verbose_name='سعر الشراء')),
                ('numberOfItem', models.IntegerField(verbose_name='العدد')),
                ('ItemPrice', models.IntegerField(verbose_name='سعر المفرد')),
                ('companyName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='pharmacy.companyname')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pharmacy.itemimage')),
                ('itemName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='pharmacy.itemname')),
                ('sourceName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='pharmacy.sourcename')),
            ],
        ),
        migrations.AddField(
            model_name='shoppingbill',
            name='item',
            field=models.ManyToManyField(related_name='Item', to='pharmacy.item'),
        ),
    ]