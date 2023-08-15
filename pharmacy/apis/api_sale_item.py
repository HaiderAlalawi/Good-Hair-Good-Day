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


@sale_item_router.put("/update/{billNumber}/{itemId}",auth=AuthBearer())
def update_item(request, edit_item:ItemCreateSchema,billNumber:str,itemId:str):
    old_item_instance=Item.objects.get(id=itemId)
    shoppingBill=ShoppingBill.objects.get(billNumber=billNumber)
    shoppingBill.item.remove(old_item_instance)
    _itemname, created=NewItemName.objects.get_or_create(name=edit_item.itemName)
    _companyname, created=NewCompanyName.objects.get_or_create(name=edit_item.companyName)
    _placeName, created=NewPlaceName.objects.get_or_create(name=edit_item.sourcePlaceName,
                                                type=edit_item.sourcePlaceType)
    _sourcename, created=NewSourceName.objects.get_or_create(name=edit_item.sourceName,placeName=_placeName)
    
    item_instance, created=Item.objects.get_or_create(
                                            itemName=_itemname,  
                                            companyName=_companyname,
                                            sourceName=_sourcename,
                                            sourcePrice=edit_item.unitPrice,
                                            numberOfItem=edit_item.numberOfItem,
                                            itemPrice=edit_item.ItemPrice,
                                            size=edit_item.notes
                                        )
    shoppingBill.item.add(item_instance)
    shoppingBill.save()
    return {200:'Sucsess edit item'} 


@sale_item_router.delete("/delete/{billNumber}/{itemId}",auth=AuthBearer())
def delete_item(request,billNumber:str,itemId:str):
    item_instance=Item.objects.get(id=itemId)
    shoppingBill=ShoppingBill.objects.get(billNumber=billNumber)
    shoppingBill.item.remove(item_instance)
    shoppingBill.save()
    return {200:'Sucsess delete item'}  