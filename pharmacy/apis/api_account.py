from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import Account, AccountCreateSchema, AccountId, GetAccounts    
from pharmacy.models import NewCompanyName, NewItemName, NewPlaceName,  NewSourceName ,ShoppingBill,Governorate,Zone,CustomerLocation,CustomerInformation,Item
from datetime import datetime

account_router = Router(tags=['Account'])

@account_router.post("/add",auth=AuthBearer())
def create_account(request, account_data:AccountCreateSchema):
    try:
        _customerinformation, created = CustomerInformation.objects.get_or_create(
                name=account_data.name)
        _governorate, created = Governorate.objects.get_or_create(
                            name=account_data.governorate)
        _zone, created = Zone.objects.get_or_create(
                            name=account_data.zone)
        _location, created= CustomerLocation.objects.get_or_create(
                    governorate=_governorate,zone=_zone,nearby=account_data.nearby)       

        _items=[]
        for item in account_data.salesItems:
            _itemname, created=NewItemName.objects.get_or_create(name=item.itemName)
            _companyname, created=NewCompanyName.objects.get_or_create(name=item.companyName)
            _placeName, created=NewPlaceName.objects.get_or_create(name=item.sourcePlaceName,
                                                type=item.sourcePlaceType)
            _sourcename, created=NewSourceName.objects.get_or_create(name=item.sourceName,placeName=_placeName)    
            __item, created=Item.objects.get_or_create(
                    itemName=_itemname,
                    companyName=_companyname,
                    sourceName=_sourcename,
                    size=item.notes,
                    sourcePrice=item.unitPrice,
                    numberOfItem=item.numberOfItem,
                    itemPrice=item.ItemPrice,
                )        
            _items.append(__item)
        if account_data.finish:
            shoppingBill=ShoppingBill.objects.create(
            customerInformation = _customerinformation,
            location=_location,
            phoneNumber=account_data.phone,
            accountLink=account_data.link,
            note= account_data.notes,
            delivary= account_data.delivary,
            deliveryPrice=account_data.delivaryPrice,
            requestDate=datetime.now(),   
            delivered=account_data.finish,
            delivaryDate=datetime.now(),
            )
            
        else:
            shoppingBill=ShoppingBill.objects.create(
            customerInformation = _customerinformation,
            location=_location,
            phoneNumber=account_data.phone,
            accountLink=account_data.link,
            note= account_data.notes,
            delivary= account_data.delivary,
            deliveryPrice=account_data.delivaryPrice,
            requestDate=datetime.now(),   
            delivered=account_data.finish,
            )
        shoppingBill.item.add(*_items)
        shoppingBill.save()
        return {200:'Sucsess add new account'}                
    except ImportError:
        return ImportError


@account_router.get("/get_all",response=GetAccounts, auth=AuthBearer())
def account_items(request):
    shoppingBills=ShoppingBill.objects.all().order_by('-requestDate')
    result=[]
    generalOutcome=0
    generalIncome=0
    for shoppingBill in shoppingBills:
        #totalItemNumber=0;
        totalAccountPrice=0
        
        if shoppingBill.delivered:
            for item in shoppingBill.item.all():
                #totalItemNumber+=item.numberOfItem
                totalAccountPrice+=(item.numberOfItem*item.itemPrice)     
        if not shoppingBill.delivered:
            for item in shoppingBill.item.all():
                #totalItemNumber+=item.numberOfItem
                totalAccountPrice+=(item.numberOfItem*item.itemPrice)
                generalOutcome+=(item.numberOfItem*item.sourcePrice)
            generalIncome+=totalAccountPrice
        if shoppingBill.delivary:
            totalAccountPrice+=shoppingBill.deliveryPrice      
        result.append({
            'id': str(shoppingBill.billNumber),'name': shoppingBill.customerInformation.name,'phone': shoppingBill.phoneNumber, 
            #'place': account.place.name,'itemsnumber':totalItemNumber,
            'total':int(totalAccountPrice),'finish':shoppingBill.delivered,'date':datetime.strftime(shoppingBill.requestDate,'%Y/%m/%d %H:%M'),
        })
    
    return {
        'income':generalIncome,
        'outcome':generalOutcome, 
        'accounts': result,
        } 


@account_router.get("/get_one/{id}",response=AccountId,auth=AuthBearer())
def get_account(request,id:str):
    shoppingBill=ShoppingBill.objects.get(billNumber=id)
    totalItemNumber=0
    delivaryPrice=0
    totalAccountPrice=0
    salesitems=[]
    for item in shoppingBill.item.all():
        salesitems+=[{
            'id':str(item.id),
            'itemName':item.itemName.name,
            'companyName':item.companyName.name,
            'sourceName':item.sourceName.name,
            'sourcePlaceName':item.sourceName.placeName.name,
            'sourcePlaceType':item.sourceName.placeName.type,
            'notes':item.size,
            'unitPrice':item.sourcePrice,
            'numberOfItem':item.numberOfItem,
            'ItemPrice':item.itemPrice,
        }]
        totalAccountPrice+=(item.numberOfItem*item.itemPrice)   
    if shoppingBill.delivary:
        delivaryPrice=shoppingBill.deliveryPrice
        totalAccountPrice+=shoppingBill.deliveryPrice
    if shoppingBill.delivered:
        delivaryDate= datetime.strftime(shoppingBill.delivaryDate,'%Y/%m/%d %H:%M') 
    else:
        delivaryDate='' 
    return {
            'id': str(shoppingBill.billNumber),'name': shoppingBill.customerInformation.name,'phone': shoppingBill.phoneNumber, 
            'governorate': shoppingBill.location.governorate.name,'zone': shoppingBill.location.zone.name,
            'nearby': shoppingBill.location.nearby,'itemsnumber':totalItemNumber,'total':int(totalAccountPrice),
            'salesItems':list(salesitems),'delivary':shoppingBill.delivary,'finish':shoppingBill.delivered,'delivaryPrice':delivaryPrice,
            'notes':shoppingBill.note,'date':datetime.strftime(shoppingBill.requestDate,'%Y/%m/%d %H:%M'),'delivaryDate':delivaryDate,
            'link':shoppingBill.accountLink
        }

@account_router.put("/update/{id}",auth=AuthBearer())
def update_account(request, edit_account:Account,id:str):
    _customerinformation, created = CustomerInformation.objects.get_or_create(
                name=edit_account.name)
    _governorate, created = Governorate.objects.get_or_create(
                            name=edit_account.governorate)
    _zone, created = Zone.objects.get_or_create(
                            name=edit_account.zone)
    _location, created= CustomerLocation.objects.get_or_create(
                    governorate=_governorate,zone=_zone,nearby=edit_account.nearby)
    shoppingBill=ShoppingBill.objects.get(billNumber=id)
    shoppingBill.customerInformation=_customerinformation
    shoppingBill.location=_location
    shoppingBill.phoneNumber=edit_account.phone
    shoppingBill.delivary=edit_account.delivary
    shoppingBill.delivered=edit_account.finish
    shoppingBill.deliveryPrice=edit_account.delivaryPrice
    shoppingBill.note=str(edit_account.notes)
    shoppingBill.accountLink=str(edit_account.link)
    if edit_account.finish:
        shoppingBill.delivaryDate=datetime.now()
    shoppingBill.save()
    return {200:'Sucsess edit account'} 

@account_router.delete("/delete/{id}",auth=AuthBearer())
def delete_Account(request,id:str):
    shoppingBill=ShoppingBill.objects.get(billNumber=id)
    shoppingBill.delete()
    return {200:'Sucsess delete account'}