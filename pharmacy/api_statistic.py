from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import *
from pharmacy.models import *
from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear

statistics_router = Router(tags=['Statistics'])




@statistics_router.get("/get_money",auth=AuthBearer())
def get_money(request):
    insidebuy=0
    insidesell=0
    outsidebuy=0
    outsidesell=0
    advertisments=0
    delivary=0
    for account in Sales.objects.all():
        if str(account.sourceName.placeName.type) == 'i':
            insidebuy+=(account.unitPrice*account.numberOfItem)
            insidesell+=(account.ItemPrice*account.numberOfItem)
        if str(account.sourceName.placeName.type) == 'o':
            outsidebuy+=(account.unitPrice*account.numberOfItem)
            outsidesell+=(account.ItemPrice*account.numberOfItem)
        if account.salesItem.delivary:
            delivary+=account.salesItem.delivaryPrice  
    for adv in Advertisment.objects.all():
            advertisments+=adv.price 
    return {'insidebuy':insidebuy, 'insidesell':insidesell,'outsidebuy':outsidebuy,
            'outsidesell':outsidesell,'advertisments':advertisments,'delivary':delivary,'myMoney':((insidesell+outsidesell)-(insidebuy+outsidebuy)-advertisments)
            }

@statistics_router.get("/get_statistics",auth=AuthBearer())
def get_statistics(request):
    result = {'items': {}, 'company': {}, 'source': {}, 'place': {}, 'date': {}, 'account':{}}

    items = ItemName.objects.annotate(
        total_items=Sum('itemName__numberOfItem'),
        total_cost=Sum(F('itemName__numberOfItem') * F('itemName__unitPrice')),
        total_sell=Sum(F('itemName__numberOfItem') * F('itemName__ItemPrice'))
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

    companies = CompanyName.objects.annotate(
        total_items=Sum('companyName__numberOfItem'),
        total_cost=Sum(F('companyName__numberOfItem') * F('companyName__unitPrice')),
        total_sell=Sum(F('companyName__numberOfItem') * F('companyName__ItemPrice'))
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
        

    sources = SourceName.objects.annotate(
        total_items=Sum('sourceName__numberOfItem'),
        total_cost=Sum(F('sourceName__numberOfItem') * F('sourceName__unitPrice')),
        total_sell=Sum(F('sourceName__numberOfItem') * F('sourceName__ItemPrice'))
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
        

    places = Sales.objects.values('salesItem__place__name').annotate(
        total_items=Sum('numberOfItem'),
        total_cost=Sum(F('numberOfItem') * F('unitPrice')),
        total_sell=Sum(F('numberOfItem') * F('ItemPrice'))
    ).exclude(total_items=None).order_by('-total_items')

    for place in places:
        result['place'][place['salesItem__place__name']] = {
            'totalItems': place['total_items'],
            'totalCost': place['total_cost'],
            'totalSell': place['total_sell']
        }
    
    accounts = Sales.objects.values('salesItem__name').annotate(
        total_items=Sum('numberOfItem'),
        total_cost=Sum(F('numberOfItem') * F('unitPrice')),
        total_sell=Sum(F('numberOfItem') * F('ItemPrice'))
                ).exclude(total_items=None).order_by('-total_items')

    # Add sales accounts to result
    for account in accounts:
        if account['salesItem__name'] in result['account']:
            # If the item already exists, add the values to the existing totals
            result['account'][account['salesItem__name']]['totalItems'] += account.total_items
            result['account'][account['salesItem__name']]['totalCost'] += account.total_cost
            result['account'][account['salesItem__name']]['totalSell'] += account.total_sell
        else:
            # Otherwise, create a new entry for the item
            result['account'][account['salesItem__name']] = {
            'totalItems': account['total_items'],
            'totalCost': account['total_cost'],
            'totalSell': account['total_sell']
        } 
        

    months = SalesAccount.objects.annotate(month=ExtractMonth('date'), year=ExtractYear('date')) \
        .values('month', 'year') \
        .annotate(total_items=Sum('salesItems__numberOfItem'),
                total_cost=Sum(F('salesItems__numberOfItem') * F('salesItems__unitPrice')),
                total_sell=Sum(F('salesItems__numberOfItem') * F('salesItems__ItemPrice'))).exclude(total_items=None).order_by('-total_items')

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