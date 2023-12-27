"""

from ninja import Router
from pharmacy.models import *

test_router = Router(tags=['Test'])

#"بغداد",
@test_router.get("/test/aaa")
def test(request):
    city_names = [ "بابل", "النجف الأشرف", "كربلاء المقدسة", "واسط", "ديالى", "الأنبار",
                "البصرة", "الديوانية", "ذي قار", "السماوة", "العمارة", "صلاح الدين", "الموصل", 
                "كركوك", "السليمانية", "أربيل", "دهوك","النجف", "كربلاء",]
    #accounts=SalesAccount.objects.all().order_by('-date')
    for account in accounts:
        var = account.place.name.split('-')
        var = [component.rstrip().lstrip() for component in var]
        
        _customerinformation, created = CustomerInformation.objects.get_or_create(
                name=account.name.lstrip().rstrip())
        _items=[]
        for item in account.salesItems.all():
            _itemname, created=ItemName.objects.get_or_create(name=item.itemName.name)
            _companyname, created=CompanyName.objects.get_or_create(name=item.companyName.name)
            _placeName, created=PlaceName.objects.get_or_create(name=item.sourceName.placeName.name,
                                                type=item.sourceName.placeName.type)
            _sourcename, created=SourceName.objects.get_or_create(name=item.sourceName.name,placeName=_placeName)    
            __item, created=Item.objects.get_or_create(
                    id=item.id,
                    itemName=_itemname,
                    companyName=_companyname,
                    sourceName=_sourcename,
                    size=item.notes,
                    sourcePrice=item.unitPrice,
                    numberOfItem=item.numberOfItem,
                    itemPrice=item.ItemPrice,
                )        
            _items.append(__item)
        if var[0] in city_names : #not baghdad
            if var[0] == 'كربلاء':
                var[0] = 'كربلاء المقدسة'  
                if var[0] == 'النجف':
                    var[0] = 'النجف الأشرف'            
            if len(var) == 4:
                _governorate, created = Governorate.objects.get_or_create(
                        name=var[0])
                _zone, created  = Zone.objects.get_or_create(
                        name=var[1])
                _location, created= CustomerLocation.objects.get_or_create(
                        governorate=_governorate,
                        zone=_zone,
                        nearby=f"{var[2]} - {var[3]}",
                    )
            
            if len(var) == 3:
                _governorate, created = Governorate.objects.get_or_create(
                        name=var[0])
                _zone, created  = Zone.objects.get_or_create(
                        name=var[1])
                _location, created= CustomerLocation.objects.get_or_create(
                        governorate=_governorate,
                        zone=_zone,
                        nearby=var[2],
                    )
            
            if len(var) == 2:
                _governorate, created = Governorate.objects.get_or_create(
                        name=var[0])
                _zone, created  = Zone.objects.get_or_create(
                        name=var[1])
                _location, created= CustomerLocation.objects.get_or_create(
                        governorate=_governorate,
                        zone=_zone,
                        nearby=None
                    )
            if len(var) == 1:
                _governorate, created = Governorate.objects.get_or_create(
                        name=var[0])
                _location, created= CustomerLocation.objects.get_or_create(
                        governorate=_governorate,
                        zone=None,
                        nearby=None
                    )                
        elif var[0] not in city_names:#baghdad
            if var[0] == 'بغداد' or var[0]=='0':
                if len(var) == 4:
                    _governorate, created = Governorate.objects.get_or_create(
                            name=var[0])
                    _zone, created = Zone.objects.get_or_create(
                            name=var[1])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=f"{var[2]} - {var[3]}",
                        )
                if len(var) == 3:
                    _governorate, created = Governorate.objects.get_or_create(
                            name=var[0])
                    _zone, created = Zone.objects.get_or_create(
                            name=var[1])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=var[2],
                        )
                if len(var) == 2:
                    _governorate, created = Governorate.objects.get_or_create(
                            name=var[0])
                    _zone, created = Zone.objects.get_or_create(
                            name=var[1])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=None
                            )
                if len(var) == 1:
                    _governorate, created = Governorate.objects.get_or_create(
                            name='بغداد')
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=None,
                            nearby=None
                            )
            else:
                if len(var) == 4:
                    _governorate, created = Governorate.objects.get_or_create(
                            name='بغداد')
                    _zone, created = Zone.objects.get_or_create(
                            name=var[0])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=f"{var[1]} - {var[2]} - {var[3]}",
                        )
                if len(var) == 3:
                    _governorate, created = Governorate.objects.get_or_create(
                            name='بغداد')
                    _zone , created= Zone.objects.get_or_create(
                            name=var[0])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=f"{var[1]} - {var[2]}",
                        )
                if len(var) == 2:
                    _governorate, created = Governorate.objects.get_or_create(
                            name='بغداد')
                    _zone, created= Zone.objects.get_or_create(
                            name=var[0])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=var[1],
                        )
                if len(var) == 1 and var[0]!='0':
                    _governorate, created = Governorate.objects.get_or_create(
                            name="بغداد")
                    _zone, created = Zone.objects.get_or_create(
                            name=var[0])
                    _location, created= CustomerLocation.objects.get_or_create(
                            governorate=_governorate,
                            zone=_zone,
                            nearby=None
                        )
        shoppingBill=ShoppingBill.objects.create(
            billNumber = account.id,
            customerInformation = _customerinformation,
            location=_location,
            phoneNumber=account.phoneNumber.lstrip().rstrip(),
            accountLink=account.link,
            note= account.notes,
            delivary= account.delivary,
            deliveryPrice=account.delivaryPrice,
            requestDate=account.date,   
            delivered=account.finish,
            delivaryDate=account.delivaryDate,
        )
        shoppingBill.item.add(*_items)
        shoppingBill.save()
    return 200 


@test_router.get("/test/bbb")
def testbbb(request):
    account=CustomerInformation.objects.get(
                name='Malak')   
    print(account)
    return 200
    
    """