# Generated by Django 4.1.7 on 2023-08-11 17:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0027_remove_customerinformation_accountlink_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Governorate',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='الرمز التسلسلي')),
                ('name', models.CharField(max_length=255, verbose_name='المحافظة')),
            ],
        ),
        migrations.AlterField(
            model_name='customerlocation',
            name='governorate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='governorate', to='pharmacy.governorate', verbose_name='المحافظة'),
        ),
    ]