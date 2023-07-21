from typing import List
from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import AdvertisementView,AdvertisementAdd
from pharmacy.models import Advertisment, AdvertismentName
from datetime import datetime


ad_router = Router(tags=['Advertisements'])



@ad_router.get("/get_all_advertisements", response=List[AdvertisementView],auth=AuthBearer())
def get_all_advertisements(request):
    result=[]
    for advertisement in Advertisment.objects.all():
        result.append({
            'id':str(advertisement.id),'name': advertisement.name.name,'price': advertisement.price,'date':datetime.strftime(advertisement.date,'%Y/%m/%d %H:%M'),
        })
    return result

@ad_router.get("/get_one/{id}", response=AdvertisementView,auth=AuthBearer())
def get_one(request,id:str):
    adv=Advertisment.objects.get(id=id)
    return {
        'id':str(adv.id),'name': adv.name.name,'price': adv.price,'date':datetime.strftime(adv.date,'%Y/%m/%d %H:%M'),
        }

@ad_router.post("/add_advertisement",auth=AuthBearer())
def add_advertisement(request,item:AdvertisementAdd):
    try:
        try:
            name=AdvertismentName.objects.get(name=item.name)
        except:
            name=AdvertismentName.objects.create(
                name=item.name
            )    
        Advertisment.objects.create(
            name=name,
            price=item.price
        )    
        return {200:'Success add new item'}                
    except ImportError:
        return ImportError
    
    
@ad_router.post("/edit_advertisement/{id}",auth=AuthBearer())
def edit_advertisement(request, edit_advertisement:AdvertisementAdd,id:str):
    try:
        try:
            name=AdvertismentName.objects.get(name=edit_advertisement.name)
        except:
            name=AdvertismentName.objects.create(
                name=edit_advertisement.name
            )    
        adv=Advertisment.objects.get(
            id=id
        )   
        adv.name=name
        adv.price= edit_advertisement.price
        adv.save()
        return {200:'Success add new item'}                
    except ImportError:
        return ImportError



@ad_router.post("/delete_advertisement/{id}",auth=AuthBearer())
def delete_advertisement(request,id:str):
    adv=Advertisment.objects.get(id=id)
    adv.delete()
    return {200:'Success delete advertisement'}      