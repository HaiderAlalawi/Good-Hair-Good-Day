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
    
class Provinces(models.TextChoices):    
    al_Anbar = 'الأنبار', 'الأنبار'
    basra = 'البصرة', 'البصرة'
    babil = 'بابل', 'بابل'
    baghdad = 'بغداد', 'بغداد'
    dahuk = 'دهوك', 'دهوك'
    diyala = 'ديالى', 'ديالى'
    dhi_Qar = 'ذي قار', 'ذي قار'
    salah_al_Din = 'صلاح الدين', 'صلاح الدين'
    karbala = 'كربلاء', 'كربلاء'
    kirkuk = 'كركوك', 'كركوك'
    maysan = 'ميسان', 'ميسان'
    najaf = 'النجف', 'النجف'
    nineveh = 'نينوى', 'نينوى'
    wasit = 'واسط', 'واسط'

class Governorate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')    
    name = models.CharField(max_length=255,verbose_name='المحافظة')
    def __str__(self):
        return f'{self.name}'

class Zone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')    
    name = models.CharField(max_length=255,verbose_name='المنطقة')
    def __str__(self):
        return f'{self.name}'
    
class CustomerLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')
    governorate= models.ForeignKey(Governorate,related_name='governorate',verbose_name='المحافظة', on_delete=models.CASCADE)
    zone =models.ForeignKey(Zone,related_name='zone', verbose_name='المنطقة',null=True, blank=True, on_delete=models.CASCADE) 
    nearby = models.CharField(max_length=255,verbose_name='اقرب نقطة دالة',null=True, blank=True,)
    def __str__(self):
        if self.zone and self.nearby is not None:
            return f'{self.governorate.name} - {self.zone.name} - {self.nearby}'
        elif self.zone is not None:
            return f'{self.governorate.name} - {self.zone.name}'
        else:
            return f'{self.governorate.name}'
    
class CustomerInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')
    name = models.CharField(max_length=255,verbose_name='اسم المشتري')
#    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return f'{self.name}'
class NewItemName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='الرمز التسلسلي')
    name= models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name}'

class NewCompanyName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='الرمز التسلسلي')
    name= models.CharField(max_length=255)
    def __str__(self):
        return f'{self.name}'
        
class NewPlaceName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='الرمز التسلسلي')
    name= models.CharField(max_length=255)
    type=models.CharField(max_length=255,choices=TypeChoices.choices,verbose_name='داخلي او خارجي')    
    def __str__(self):
        return f'{self.name} - {self.type}'
    
class NewSourceName(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='الرمز التسلسلي')
    name= models.CharField(max_length=255)
    placeName=models.ForeignKey(NewPlaceName,related_name='placeName', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} - {self.placeName.name} - {self.placeName.type}'


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='الرمز التسلسلي')
    #editable=False,auto_created=True,
    itemName=models.ForeignKey(NewItemName,related_name='item', on_delete=models.CASCADE)
    companyName=models.ForeignKey(NewCompanyName,related_name='company', on_delete=models.CASCADE)
    sourceName=models.ForeignKey(NewSourceName,related_name='source', on_delete=models.CASCADE)
    size = models.CharField(max_length=200,null=True, blank=True)
#    description = models.TextField(null=True, blank=True,verbose_name='الوصف')
    sourcePrice= models.IntegerField(verbose_name='سعر الشراء')
    numberOfItem= models.IntegerField(verbose_name='العدد')
    itemPrice= models.IntegerField(verbose_name='سعر المفرد')
#    hidden = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.itemName}'

#class ItemImage(models.Model):
#    image = models.ImageField(upload_to='images\item')
#    item = models.ForeignKey(Item,related_name='images', on_delete=models.CASCADE)

    
class ShoppingBill(models.Model):
    billNumber = models.CharField(max_length=20, unique=True,primary_key=True,auto_created=True,editable=False)
    customerInformation = models.ForeignKey(CustomerInformation,related_name='customerInformation', on_delete=models.CASCADE)
    location = models.ForeignKey(CustomerLocation,related_name='accountPlace', verbose_name="العنوان", on_delete=models.CASCADE)    
    phoneNumber = models.CharField(max_length=50,verbose_name='رقم الهاتف')
    accountLink= models.TextField(null=True, blank=True,verbose_name='رابط') 
    note = models.TextField(null=True, blank=True,verbose_name='ملاحظات')
    delivary = models.BooleanField(default=False)
    deliveryPrice = models.IntegerField(verbose_name='سعر التوصيل',default=0,null=True, blank=True)
    requestDate = models.DateTimeField(verbose_name='تاريخ الطلب',auto_created=True,auto_now=True)
    #confirmation = models.BooleanField(default=False)
    #confirmationDate = models.DateTimeField(verbose_name='تاريخ تاكيد الطلب', null=True, blank=True)
    delivered = models.BooleanField(default=False)
    delivaryDate = models.DateTimeField(verbose_name='تاريخ التوصيل', null=True, blank=True)
    item = models.ManyToManyField(Item, related_name='items')


    def save(self, *args, **kwargs):
        if not self.billNumber:
            current_date = timezone.now().strftime('%Y%m%d')
            random_chars = generate_random_chars(4)
            #count = ShoppingBill.objects.filter(requestDate__date=timezone.now().date()).count() + 1
            self.billNumber = f'{current_date}{random_chars}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.billNumber} - {self.customerInformation}'


class OutcomeName(models.Model):
    name= models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Outcome(models.Model):
    name=models.ForeignKey(OutcomeName,related_name='advertisment', on_delete=models.CASCADE)
    price= models.IntegerField()
    date= models.DateTimeField(verbose_name='التاريخ',auto_now=True)
    
    def __str__(self):
        return self.name.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,auto_created=True,verbose_name='الرمز التسلسلي')
    name = models.CharField(max_length=255)
    company = models.ForeignKey(NewCompanyName, on_delete=models.CASCADE)
    details= models.CharField(max_length=700,null=True, blank=True)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name