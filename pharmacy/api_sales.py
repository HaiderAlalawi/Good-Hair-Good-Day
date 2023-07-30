from typing import List
from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import *
from pharmacy.models import *
from datetime import datetime
from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear

sales_router = Router(tags=['Sales'])



@sales_router.get("/get_accounts", auth=AuthBearer())
def get_accounts(request):
    accounts=SalesAccount.objects.all().order_by('-date')
    result=[]
    generalOutcome=0
    generalIncome=0
    for account in accounts:
        #totalItemNumber=0;
        totalAccountPrice=0
        
        if account.finish:
            for item in account.salesItems.all():
                #totalItemNumber+=item.numberOfItem
                totalAccountPrice+=(item.numberOfItem*item.ItemPrice)     
        if not account.finish:
            for item in account.salesItems.all():
                #totalItemNumber+=item.numberOfItem
                totalAccountPrice+=(item.numberOfItem*item.ItemPrice)
                generalOutcome+=(item.numberOfItem*item.unitPrice)
        generalIncome+=totalAccountPrice
        if account.delivary:
            totalAccountPrice+=account.delivaryPrice      
        result.append({
            'id': str(account.id),'name': account.name,'phone': account.phoneNumber, 
            #'place': account.place.name,'itemsnumber':totalItemNumber,
            'total':int(totalAccountPrice),'finish':account.finish,'date':datetime.strftime(account.date,'%Y/%m/%d %H:%M'),
        })
    
    return {
        'income':generalIncome,
        'outcome':generalOutcome, 
        'accounts': result,
        } 


@sales_router.get("/get_account/{id}",response=AccountId,auth=AuthBearer())
def get_account(request,id:str):
    account=SalesAccount.objects.get(id=id)
    totalItemNumber=0
    delivaryPrice=0
    totalAccountPrice=0
    salesitems=[]
    for item in account.salesItems.all():
        salesitems+=[{
            'id':str(item.id),
            'itemName':item.itemName.name,
            'companyName':item.companyName.name,
            'sourceName':item.sourceName.name,
            'sourcePlaceName':item.sourceName.placeName.name,
            'sourcePlaceType':item.sourceName.placeName.type,
            'notes':item.notes,
            'unitPrice':item.unitPrice,
            'numberOfItem':item.numberOfItem,
            'ItemPrice':item.ItemPrice,
        }]
        totalAccountPrice+=(item.numberOfItem*item.ItemPrice)
    if account.delivary:
        delivaryPrice=account.delivaryPrice
        totalAccountPrice+=account.delivaryPrice
    if account.finish:
        delivaryDate= datetime.strftime(account.delivaryDate,'%Y/%m/%d %H:%M') 
    else:
        delivaryDate='' 
    return {
            'id': str(account.id),'name': account.name,'phone': account.phoneNumber, 'place': account.place.name,'itemsnumber':totalItemNumber,'total':int(totalAccountPrice),'salesItems':list(salesitems),
            'delivary':account.delivary,'finish':account.finish,'delivaryPrice':delivaryPrice,'notes':account.notes,'date':datetime.strftime(account.date,'%Y/%m/%d %H:%M'),'delivaryDate':delivaryDate,
            'link':account.link
        }


@sales_router.post("/add_account",auth=AuthBearer())
def add_account(request, accountData:AccountAdd):
    try:
        try:
            place=PlaceAccountName.objects.get(name=accountData.place)
        except:
            place=PlaceAccountName.objects.create(name=accountData.place)
        if accountData.finish:
            account=SalesAccount.objects.create(
            name=accountData.name,
            place=place,
            phoneNumber=accountData.phone,
            delivary=accountData.delivary,
            finish=accountData.finish,
            delivaryPrice=accountData.delivaryPrice,
            notes=str(accountData.notes),
            link=str(accountData.link),
            delivaryDate=datetime.now(),
            date=datetime.now() 
            )
        else:
            account=SalesAccount.objects.create(
            name=accountData.name,
            place=place,
            phoneNumber=accountData.phone,
            delivary=accountData.delivary,
            finish=accountData.finish,
            delivaryPrice=accountData.delivaryPrice,
            notes=str(accountData.notes),
            link=str(accountData.link),
            date=datetime.now() 
                )
        for item in accountData.salesItems:
            try:
                name=ItemName.objects.get(name=item.itemName)
            except:
                name=ItemName.objects.create(
                    name=item.itemName
                ) 
            try:
                companyname=CompanyName.objects.get(name=item.companyName)
            except:  
                companyname=CompanyName.objects.create(
                    name=item.companyName
                )
            try:
                placeName=PlaceName.objects.get(name=item.sourcePlaceName,type=item.sourcePlaceType)
            except:  
                placeName=PlaceName.objects.create(
                    name=item.sourcePlaceName,
                    type=item.sourcePlaceType
                )                  
            try:
                sourcename=SourceName.objects.get(name=item.sourceName,placeName=placeName)
            except:  
                sourcename=SourceName.objects.create(
                    name=item.sourceName,
                    placeName=placeName
                )            
                
            Sales.objects.create(
            itemName=name,
            companyName=companyname,
            sourceName=sourcename,
            unitPrice=item.unitPrice,
            numberOfItem=item.numberOfItem,
            ItemPrice=item.ItemPrice,
            notes=item.notes,
            salesItem=account
        )
        return {200:'Sucsess add new account'}                
    except ImportError:
        return ImportError


@sales_router.post("/add_item",auth=AuthBearer())
def add_item(request,id:str,item:SalesItem):
    try:
        account=SalesAccount.objects.get(id=id)
        try:
            name=ItemName.objects.get(name=item.itemName)
        except:
            name=ItemName.objects.create(
                    name=item.itemName
                ) 
        try:
                companyname=CompanyName.objects.get(name=item.companyName)
        except:  
                companyname=CompanyName.objects.create(
                    name=item.companyName
                )
        try:
                placeName=PlaceName.objects.get(name=item.sourcePlaceName,type=item.sourcePlaceType)
        except:  
                placeName=PlaceName.objects.create(
                    name=item.sourcePlaceName,
                    type=item.sourcePlaceType
                )                  
        try:
                sourcename=SourceName.objects.get(name=item.sourceName,placeName=placeName)
        except:  
                sourcename=SourceName.objects.create(
                    name=item.sourceName,
                    placeName=placeName
                )            
                
        Sales.objects.create(
            itemName=name,
            companyName=companyname,
            sourceName=sourcename,
            unitPrice=item.unitPrice,
            numberOfItem=item.numberOfItem,
            ItemPrice=item.ItemPrice,
            notes=item.notes,
            salesItem=account
        )
        return {200:'Sucsess add new item'}                
    except ImportError:
        return ImportError

@sales_router.post("/edit_account",auth=AuthBearer())
def edit_account(request, edit_account:Account,id:str):
    try: 
        place=PlaceAccountName.objects.get(name=edit_account.place)
    except:
        place=PlaceAccountName.objects.create(name=edit_account.place)   
    account=SalesAccount.objects.get(id=id)
    account.name=edit_account.name
    account.place=place
    account.phoneNumber=edit_account.phone
    account.delivary=edit_account.delivary
    account.finish=edit_account.finish
    account.delivaryPrice=edit_account.delivaryPrice
    account.notes=str(edit_account.notes)
    account.link=str(edit_account.link)
    if edit_account.finish:
        account.delivaryDate=datetime.now()
    account.save()
    return {200:'Sucsess edit account'} 


@sales_router.post("/edit_item",auth=AuthBearer())
def edit_item(request, edit_item:SalesItem,id:str):
    try: 
        itemName=ItemName.objects.get(name=edit_item.itemName)
    except:
        itemName=ItemName.objects.create(name=edit_item.itemName) 
    try: 
        companyName=CompanyName.objects.get(name=edit_item.companyName)
    except:
        companyName=CompanyName.objects.create(name=edit_item.companyName) 
    try:
        placeName=PlaceName.objects.get(name=edit_item.sourcePlaceName,
                                        type=edit_item.sourcePlaceType)
    except:  
        placeName=PlaceName.objects.create(
            name=edit_item.sourcePlaceName,
            type=edit_item.sourcePlaceType
        )                  
    try:
        sourcename=SourceName.objects.get(name=edit_item.sourceName,placeName=placeName)
    except:  
        sourcename=SourceName.objects.create(
            name=edit_item.sourceName,
            placeName=placeName
        )
    item=Sales.objects.get(id=id)
    item.itemName=itemName
    item.companyName=companyName
    item.sourceName=sourcename
    item.unitPrice=edit_item.unitPrice
    item.numberOfItem=edit_item.numberOfItem
    item.ItemPrice=edit_item.ItemPrice
    item.notes=edit_item.notes
    item.save()   
    return {200:'Sucsess edit account'} 


@sales_router.post("/delete_Account/{id}",auth=AuthBearer())
def delete_Account(request,id:str):
    account=SalesAccount.objects.get(id=id)
    account.delete()
    return {200:'Sucsess delete account'}

@sales_router.post("/delete_Item/{id}",auth=AuthBearer())
def delete_Item(request,id:str):
    account=Sales.objects.get(id=id)
    account.delete()
    return {200:'Sucsess delete item'}  


