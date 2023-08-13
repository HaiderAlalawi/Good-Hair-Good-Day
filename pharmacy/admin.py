# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Governorate, Zone, CustomerLocation, CustomerInformation, NewItemName, NewCompanyName, NewPlaceName, NewSourceName, Item, ShoppingBill, OutcomeName, Outcome, Product


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
    search_fields = ('name',)


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
    raw_id_fields = ('itemName', 'companyName', 'sourceName')


@admin.register(ShoppingBill)
class ShoppingBillAdmin(admin.ModelAdmin):
    list_display = (
        'requestDate',
        'billNumber',
        'customerInformation',
        'location',
        'phoneNumber',
        'accountLink',
        'note',
        'delivary',
        'deliveryPrice',
        'delivered',
        'delivaryDate',
    )
    list_filter = ('requestDate', 'delivary', 'delivered', 'delivaryDate')
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
