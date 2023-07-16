import uuid
from django.db import models
from django.utils import timezone
import random
import string

# Create your models here.
    # def myDate(self, obj):
    #    return obj.date.strftime('%Y/%m/%d %H:%M')
    
def generate_random_chars(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))    
class TypeChoices(models.TextChoices):
    inside='i','داخلي'
    outside='o','خارجي'
    
class PlaceAccountName(models.Model):
    name= models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name}'
    
class SalesAccount(models.Model):
    id = models.CharField(max_length=20, unique=True,primary_key=True,auto_created=True,editable=False)
    name= models.CharField(max_length=255,verbose_name='اسم المشتري')
    place=models.ForeignKey(PlaceAccountName,related_name='accountPlace', verbose_name="العنوان", on_delete=models.CASCADE)
    phoneNumber=models.CharField(max_length=255,verbose_name='رقم الهاتف')
    notes= models.TextField(null=True, blank=True,verbose_name='ملاحظات')  
    link= models.TextField(null=True, blank=True,verbose_name='رابط')  
    date= models.DateTimeField(verbose_name='التاريخ')
    delivary=models.BooleanField(default=False,)
    finish=models.BooleanField(default=False)
    delivaryPrice= models.IntegerField(verbose_name='سعر التوصيل',default=0,null=True, blank=True)
    delivaryDate= models.DateTimeField(verbose_name='تاريخ التوصيل',null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            current_date = timezone.now().strftime('%Y%m%d')
            random_chars = generate_random_chars(4)
            self.id = f'{current_date}{random_chars}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'



class ItemName(models.Model):
    name= models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name}'
    
class CompanyName(models.Model):
    name= models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name}'
        
class PlaceName(models.Model):
    name= models.CharField(max_length=255)
    type=models.CharField(max_length=255,choices=TypeChoices.choices,verbose_name='داخلي او خارجي')    
    def __str__(self):
        return f'{self.name} - {self.type}'
    
class SourceName(models.Model):
    name= models.CharField(max_length=255)
    placeName=models.ForeignKey(PlaceName,related_name='placeName', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} - {self.placeName.name} - {self.placeName.type}'


class Sales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')
    itemName=models.ForeignKey(ItemName,related_name='itemName', on_delete=models.CASCADE)
    companyName=models.ForeignKey(CompanyName,related_name='companyName', on_delete=models.CASCADE)
    sourceName=models.ForeignKey(SourceName,related_name='sourceName', on_delete=models.CASCADE)
    notes= models.CharField(max_length=700,null=True, blank=True)
    unitPrice= models.IntegerField(verbose_name='سعر الشراء')
    numberOfItem= models.IntegerField(verbose_name='العدد')
    ItemPrice= models.IntegerField(verbose_name='سعر المفرد')
    salesItem=models.ForeignKey(SalesAccount,related_name='salesItems', verbose_name="المواد", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.itemName}'


class AdvertismentName(models.Model):
    name= models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Advertisment(models.Model):
    name=models.ForeignKey(AdvertismentName,related_name='advertisment', on_delete=models.CASCADE)
    price= models.IntegerField()
    date= models.DateTimeField(verbose_name='التاريخ',auto_now=True)
    
    def __str__(self):
        return self.name.name


#how to use nofication from django to flutter app?
