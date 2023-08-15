from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import  ItemCreateSchema  
from pharmacy.models import NewCompanyName, NewItemName, NewPlaceName,NewSourceName,ShoppingBill,Item

sale_item_router = Router(tags=['SaleItem'])

@sale_item_router.post("/add/{id}",auth=AuthBearer())
def create_item(request,id:str,item:ItemCreateSchema):
    try:
        shoppingBill=ShoppingBill.objects.get(billNumber=id)
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
        shoppingBill.item.add(__item)
        shoppingBill.save()
        return {200:'Sucsess add new item'}                
    except ImportError:
        return ImportError


@sale_item_router.put("/update/{id}",auth=AuthBearer())
def update_item(request, edit_item:ItemCreateSchema,id:str):
    _itemname, created=NewItemName.objects.get_or_create(name=edit_item.itemName)
    _companyname, created=NewCompanyName.objects.get_or_create(name=edit_item.companyName)
    _placeName, created=NewPlaceName.objects.get_or_create(name=edit_item.sourcePlaceName,
                                                type=edit_item.sourcePlaceType)
    _sourcename, created=NewSourceName.objects.get_or_create(name=edit_item.sourceName,placeName=_placeName)
    
    item_instance=Item.objects.get(id=id)
    item_instance.itemName=_itemname
    item_instance.companyName=_companyname
    item_instance.sourceName=_sourcename
    item_instance.sourcePrice=edit_item.unitPrice
    item_instance.numberOfItem=edit_item.numberOfItem
    item_instance.itemPrice=edit_item.ItemPrice
    item_instance.size=edit_item.notes
    item_instance.save()   
    return {200:'Sucsess edit account'} 


@sale_item_router.delete("/delete/{billNumber}/{itemId}",auth=AuthBearer())
def delete_item(request,billNumber:str,itemId:str):
    item_instance=Item.objects.get(id=itemId)
    shoppingBill=ShoppingBill.objects.get(billNumber=billNumber)
    shoppingBill.item.remove(item_instance)
    return {200:'Sucsess delete item'}  