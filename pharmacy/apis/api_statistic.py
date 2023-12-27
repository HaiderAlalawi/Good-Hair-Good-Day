from typing import List
from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.models import Outcome,NewItemName,NewCompanyName,NewSourceName,Item,ShoppingBill
from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from pharmacy.schema import ItemsNotDeleverd

statistics_router = Router(tags=['Statistics'])

@statistics_router.get("/get_items",response=List[ItemsNotDeleverd],auth=AuthBearer())
def items_not_deleverd(request):
    shoppingBills = ShoppingBill.objects.select_related('customerInformation',
                                                    'location',
                                                    'location__governorate',
                                                    'location__zone',
                                                    ).filter(delivered=False)

    # Use a dictionary to group items by their unique characteristics
    item_groups = {}

    for shoppingBill in shoppingBills:
        for item in shoppingBill.item.select_related(
                'itemName',
                'companyName',
                'sourceName',
                'sourceName__placeName',
                'size',
                'sourcePrice',
                'numberOfItem',
                'itemPrice',
                ).all():
            item_key = (
                item.itemName.name,
                item.companyName.name,
                item.sourceName.name,
                item.sourceName.placeName.name,
                item.sourceName.placeName.type,
                item.size.size
            )

            # Construct the nameNumber value
            name_number = f'{shoppingBill.customerInformation.name} ({item.numberOfItem.number})'
            item_total_number = item.numberOfItem.number  # Get the item's total number

            if item_key not in item_groups:
                item_groups[item_key] = {
                    'itemName': item.itemName.name,
                    'companyName': item.companyName.name,
                    'sourceName': item.sourceName.name,
                    'sourcePlaceName': item.sourceName.placeName.name,
                    'sourcePlaceType': item.sourceName.placeName.type,
                    'notes': item.size.size,
                    'totalNumber': item_total_number,  # Add the total number
                    'nameNumbers': [name_number]
                }
            else:
                item_groups[item_key]['nameNumbers'].append(name_number)
                # Increment the total number for the existing item group
                item_groups[item_key]['totalNumber'] += item_total_number

    # Convert the dictionary to a list of items
    salesitems = list(item_groups.values())

    return salesitems

@statistics_router.get("/get_money",auth=AuthBearer())
def get_money(request):
    insidebuy=0
    insidesell=0
    outsidebuy=0
    outsidesell=0
    allOutcome=0
    allDelivary=0
    for shoppingBill in ShoppingBill.objects.select_related('customerInformation',
                                                    'location',
                                                    'location__governorate',
                                                    'location__zone',
                                                    ).all():
        for item in shoppingBill.item.select_related(
                'itemName',
                'companyName',
                'sourceName',
                'sourceName__placeName',
                'size',
                'sourcePrice',
                'numberOfItem',
                'itemPrice',
                ).all():
            if str(item.sourceName.placeName.type) == 'i':
                insidebuy+=(item.sourcePrice.price*item.numberOfItem.number)
                insidesell+=(item.itemPrice.price*item.numberOfItem.number)
            if str(item.sourceName.placeName.type) == 'o':
                outsidebuy+=(item.sourcePrice.price*item.numberOfItem.number)
                outsidesell+=(item.itemPrice.price*item.numberOfItem.number)
        if shoppingBill.delivary:
            allDelivary+=shoppingBill.deliveryPrice  
    for outcome in Outcome.objects.select_related('name',
                                                    
                                                    ).all():
            allOutcome+=outcome.price 
    return {'insidebuy':insidebuy, 'insidesell':insidesell,'outsidebuy':outsidebuy,
            'outsidesell':outsidesell,'advertisments':allOutcome,'delivary':allDelivary,'myMoney':((insidesell+outsidesell)-(insidebuy+outsidebuy)-allOutcome)
            }

@statistics_router.get("/get_statistics",auth=AuthBearer())
def get_statistics(request):
    result = {'items': {}, 'company': {}, 'source': {}, 'place': {}, 'date': {}, 'account':{}}

    items = NewItemName.objects.annotate(
        total_items=Sum('item__numberOfItem__number'),
        total_cost=Sum(F('item__numberOfItem__number') * F('item__sourcePrice__price')),
        total_sell=Sum(F('item__numberOfItem__number') * F('item__itemPrice__price'))
    ).exclude(total_items=None).order_by('-total_items')

    for item in items:
        if item.name in result['items']:
            # If the item already exists, add the values to the existing totals
            result['items'][item.name]['totalItems'] += item.total_items
            result['items'][item.name]['totalCost'] += item.total_cost
            result['items'][item.name]['totalSell'] += item.total_sell
        else:
            # Otherwise, create a new entry for the item
            result['items'][item.name] = {
                'totalItems': item.total_items,
                'totalCost': item.total_cost,
                'totalSell': item.total_sell
            }

    companies = NewCompanyName.objects.annotate(
        total_items=Sum('company__numberOfItem__number'),
        total_cost=Sum(F('company__numberOfItem__number') * F('company__sourcePrice__price')),
        total_sell=Sum(F('company__numberOfItem__number') * F('company__itemPrice__price'))
    ).exclude(total_items=None).order_by('-total_items')

    for company in companies:
        if company.name in result['company']:
            # If the item already exists, add the values to the existing totals
            result['company'][company.name]['totalItems'] += item.total_items
            result['company'][company.name]['totalCost'] += item.total_cost
            result['company'][company.name]['totalSell'] += item.total_sell
        else:
            # Otherwise, create a new entry for the item
            result['company'][company.name] = {
            'totalItems': company.total_items,
            'totalCost': company.total_cost,
            'totalSell': company.total_sell
            }
        

    sources = NewSourceName.objects.annotate(
        total_items=Sum('source__numberOfItem__number'),
        total_cost=Sum(F('source__numberOfItem__number') * F('source__sourcePrice__price')),
        total_sell=Sum(F('source__numberOfItem__number') * F('source__itemPrice__price'))
    ).exclude(total_items=None).order_by('-total_items')

    for source in sources:
        if source.name in result['source']:
            # If the item already exists, add the values to the existing totals
            result['source'][source.name]['totalItems'] += source.total_items
            result['source'][source.name]['totalCost'] += source.total_cost
            result['source'][source.name]['totalSell'] += source.total_sell
        else:
            # Otherwise, create a new entry for the item
            result['source'][source.name] = {
            'totalItems': source.total_items,
            'totalCost': source.total_cost,
            'totalSell': source.total_sell
        }
        

    places = Item.objects.select_related(
                'itemName',
                'companyName',
                'sourceName',
                'sourceName__placeName',
                'size',
                'sourcePrice',
                'numberOfItem',
                'itemPrice',
                ).values('items__location__governorate__name').annotate(
        total_items=Sum('numberOfItem__number'),
        total_cost=Sum(F('numberOfItem__number') * F('sourcePrice__price')),
        total_sell=Sum(F('numberOfItem__number') * F('itemPrice__price'))
    ).exclude(total_items=None).order_by('-total_items')

    for place in places:
        result['place'][place['items__location__governorate__name']] = {
            'totalItems': place['total_items'],
            'totalCost': place['total_cost'],
            'totalSell': place['total_sell']
        }
    
    accounts = Item.objects.select_related(
                'itemName',
                'companyName',
                'sourceName',
                'sourceName__placeName',
                'size',
                'sourcePrice',
                'numberOfItem',
                'itemPrice',
                ).values('items__customerInformation__name').annotate(
        total_items=Sum('numberOfItem__number'),
        total_cost=Sum(F('numberOfItem__number') * F('sourcePrice__price')),
        total_sell=Sum(F('numberOfItem__number') * F('itemPrice__price'))
                ).exclude(total_items=None).order_by('-total_items')

    # Add sales accounts to result
    for account in accounts:
        if account['items__customerInformation__name'] in result['account']:
            # If the item already exists, add the values to the existing totals
            result['account'][account['items__customerInformation__name']]['totalItems'] += account.total_items
            result['account'][account['items__customerInformation__name']]['totalCost'] += account.total_cost
            result['account'][account['items__customerInformation__name']]['totalSell'] += account.total_sell
        else:
            # Otherwise, create a new entry for the item
            result['account'][account['items__customerInformation__name']] = {
            'totalItems': account['total_items'],
            'totalCost': account['total_cost'],
            'totalSell': account['total_sell']
        } 
        

    months = ShoppingBill.objects.select_related('customerInformation',
                                                    'location',
                                                    'location__governorate',
                                                    'location__zone',
                                                    ).annotate(month=ExtractMonth('requestDate'), year=ExtractYear('requestDate')) \
        .values('month', 'year') \
        .annotate(total_items=Sum('item__numberOfItem__number'),
                total_cost=Sum(F('item__numberOfItem__number') * F('item__sourcePrice__price')),
                total_sell=Sum(F('item__numberOfItem__number') * F('item__itemPrice__price'))).exclude(total_items=None).order_by('-total_items')

    for month in months:
        year = month['year']
        month_num = month['month']
        total_items = month['total_items']
        total_cost = month['total_cost']
        total_sell = month['total_sell']

        if year not in result['date']:
            result['date'][year] = {}

        result['date'][year][month_num] = {
            'totalItems': total_items,
            'totalCost': total_cost,
            'totalSell': total_sell
        }
    return result    