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


class ItemCreateSchema(Schema):
    itemName: str
    companyName: str
    sourceName: str
    sourcePlaceName: str
    sourcePlaceType: str
    notes:str | None
    unitPrice:int
    numberOfItem:int
    ItemPrice:int



class SalesItemId(ItemCreateSchema):
    id:str

class Account(Schema):
    name:str
    phone:str
    governorate:str
    zone:str | None
    nearby: str | None
    delivary:bool
    finish:bool
    delivaryPrice:int
    notes:str | None
    link:str | None

class AccountCreateSchema(Account):
    salesItems:List[ItemCreateSchema]

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


class GetAccounts(Schema):
    income:int
    outcome:int
    accounts:List[AllAccount]




class OutcomeView(Schema):
    id:str
    name:str
    price:int
    date:str

class OutcomeCreateSchema(Schema):
    name:str
    price:int
    
class ProductSchema(Schema):
    name: str
    company_name: str
    details : str | None
    buy_price: float
    sale_price: float    



class ProductResponseSchema(ProductSchema):
    id: str
    
class ProductCreateSchema(ProductSchema):
    pass    