# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Governorate, Zone, CustomerLocation, CustomerInformation, NewItemName, NewCompanyName, NewPlaceName, NewSourceName, NewSize, NewPrice, NewNumberOfItem, Item, ShoppingBill, OutcomeName, Outcome, Product


@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CustomerLocation)
class CustomerLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'governorate', 'zone', 'nearby')
    raw_id_fields = ('governorate', 'zone')


@admin.register(CustomerInformation)
class CustomerInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(NewItemName)
class NewItemNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(NewCompanyName)
class NewCompanyNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(NewPlaceName)
class NewPlaceNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    search_fields = ('name',)


@admin.register(NewSourceName)
class NewSourceNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'placeName')
    list_filter = ('placeName',)
    search_fields = ('name',)


@admin.register(NewSize)
class NewSizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')


@admin.register(NewPrice)
class NewPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')


@admin.register(NewNumberOfItem)
class NewNumberOfItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'itemName',
        'companyName',
        'sourceName',
        'size',
        'sourcePrice',
        'numberOfItem',
        'itemPrice',
    )
    raw_id_fields = (
        'itemName',
        'companyName',
        'sourceName',
        'size',
        'sourcePrice',
        'numberOfItem',
        'itemPrice',
    )


@admin.register(ShoppingBill)
class ShoppingBillAdmin(admin.ModelAdmin):
    list_display = (
        'billNumber',
        'customerInformation',
        'location',
        'phoneNumber',
        'accountLink',
        'note',
        'delivary',
        'deliveryPrice',
        'requestDate',
        'delivered',
        'delivaryDate',
    )
    list_filter = ('delivary', 'requestDate', 'delivered', 'delivaryDate')
    raw_id_fields = ('customerInformation', 'location')


@admin.register(OutcomeName)
class OutcomeNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'date')
    list_filter = ('name', 'date')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'company',
        'details',
        'buy_price',
        'sale_price',
    )
    list_filter = ('company',)
    search_fields = ('name',)
