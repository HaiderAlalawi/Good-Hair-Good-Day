"""

from django.db import migrations, models


def trim_spaces(apps, schema_editor):
    models_to_update = [
        ('pharmacy', 'PlaceAccountName'),
        ('pharmacy', 'SalesAccount'),
        ('pharmacy', 'ItemName'),
        ('pharmacy', 'CompanyName'),
        ('pharmacy', 'PlaceName'),
        ('pharmacy', 'SourceName'),
        ('pharmacy', 'Sales'),
        ('pharmacy', 'AdvertismentName'),
        ('pharmacy', 'Advertisment'),
    ]

    for app_name, model_name in models_to_update:
        Model = apps.get_model(app_name, model_name)
        objects = Model.objects.all()
        for obj in objects:
            for field in obj._meta.fields:
                if isinstance(field, (models.CharField, models.TextField)):
                    value = getattr(obj, field.name)
                    if value:
                        setattr(obj, field.name, value.strip())
            obj.save()
    print('success!!!')        


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0006_salesaccount_link_alter_salesaccount_date'),
    ]

    operations = [
        migrations.RunPython(trim_spaces),
    ]
    
"""
