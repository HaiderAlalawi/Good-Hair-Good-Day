from typing import List
from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.schema import OutcomeView,OutcomeCreateSchema
from pharmacy.models import Outcome, OutcomeName
from datetime import datetime


outcome_router = Router(tags=['Outcome'])

@outcome_router.post("/",auth=AuthBearer())
def create_outcome(request,outcome:OutcomeCreateSchema):
    try:
        try:
            name=OutcomeName.objects.get(name=outcome.name)
        except:
            name=OutcomeName.objects.create(
                name=outcome.name
            )    
        Outcome.objects.create(
            name=name,
            price=outcome.price
        )    
        return {200:'Success add new item'}                
    except ImportError:
        return ImportError
    

@outcome_router.get("/", response=List[OutcomeView],auth=AuthBearer())
def outcome_items(request):
    result=[]
    for outcome in Outcome.objects.all():
        result.append({
            'id':str(outcome.id),'name': outcome.name.name,'price': outcome.price,'date':datetime.strftime(outcome.date,'%Y/%m/%d %H:%M'),
        })
    return result

@outcome_router.get("/{id}", response=OutcomeView,auth=AuthBearer())
def get_outcome(request,id:str):
    outcome=Outcome.objects.get(id=id)
    return {
        'id':str(outcome.id),'name': outcome.name.name,'price': outcome.price,'date':datetime.strftime(outcome.date,'%Y/%m/%d %H:%M'),
        }


    
@outcome_router.put("/{id}",auth=AuthBearer())
def update_outcome(request, outcome:OutcomeCreateSchema,id:str):
    try:
        try:
            name=OutcomeName.objects.get(name=outcome.name)
        except:
            name=OutcomeName.objects.create(
                name=outcome.name
            )    
        outcome_instance=Outcome.objects.get(
            id=id
        )   
        outcome_instance.name=name
        outcome_instance.price= outcome.price
        outcome_instance.save()
        return {200:'Success edit item'}                
    except ImportError:
        return ImportError



@outcome_router.delete("/{id}",auth=AuthBearer())
def delete_outcome(request,id:str):
    outcome_instance=Outcome.objects.get(id=id)
    outcome_instance.delete()
    return {200:'Success delete advertisement'}      