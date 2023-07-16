# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *


@admin.register(SalesAccount)
class SalesAccountAdmin(admin.ModelAdmin):
    def myDate(self, obj):
        return obj.date.strftime('%Y/%m/%d %H:%M')
    list_display = (
        'id',
        'name',
        'place',
        'phoneNumber',
        'notes',
        'date',
        'delivaryDate',
        'delivary',
        'finish',
        'delivaryPrice',
        'link',
    )
    list_filter = ('date', 'delivary', 'finish','place')
    search_fields = ('name','id')




@admin.register(ItemName)
class ItemNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CompanyName)
class CompanyNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(PlaceName)
class PlaceNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    search_fields = ('name',)


@admin.register(SourceName)
class SourceNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'placeName')
    list_filter = ('placeName',)
    search_fields = ('name',)


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'itemName',
        'companyName',
        'sourceName',
        'notes',
        'unitPrice',
        'numberOfItem',
        'ItemPrice',
        'salesItem',
    )
    list_filter = ('itemName', 'companyName', 'sourceName', 'salesItem')


@admin.register(AdvertismentName)
class AdvertismentNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Advertisment)
class AdvertismentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'date')
    list_filter = ('name', 'date')
    search_fields = ('name',)
    
@admin.register(PlaceAccountName)
class PlaceAccountName(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
