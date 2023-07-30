from typing import List
from ninja import Schema


class SignIn(Schema):
    username=str
    password=str

class AuthOut(Schema):
    token: str

class ErrorCode(Schema):
    detail: str


class Error(Schema):
    details:str


class SalesItem(Schema):
    itemName: str
    companyName: str
    sourceName: str
    sourcePlaceName: str
    sourcePlaceType: str
    notes:str | None
    unitPrice:int
    numberOfItem:int
    ItemPrice:int



class SalesItemId(SalesItem):
    id:str

class Account(Schema):
    name:str
    phone:str
    place: str
    delivary:bool
    finish:bool
    delivaryPrice:int
    notes:str | None
    link:str | None

class AccountAdd(Account):
    salesItems:List[SalesItem]

class AccountView(Account):
    itemsnumber:int  
    total:int 
    salesItems:List[SalesItemId]
    date:str
    delivaryDate:str | None


class AccountId(AccountView):
    id:str


class AllAccount(Schema):
    id:str
    name:str
    phone:str
    #place: str
    #itemsnumber:int  
    total:int 
    finish:bool
    date:str
    totalOutcome:int







class AdvertisementView(Schema):
    id:str
    name:str
    price:int
    date:str

class AdvertisementAdd(Schema):
    name:str
    price:int



