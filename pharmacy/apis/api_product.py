# myapp/api.py
from ninja import Router
from pharmacy.authorization import AuthBearer
from pharmacy.models import Product, NewCompanyName
from pharmacy.schema import ProductSchema, ProductResponseSchema, ProductCreateSchema

product_router = Router(tags=['Products'])

@product_router.post("/",auth=AuthBearer())
def create_product(request, product: ProductCreateSchema):
    try:
        company = NewCompanyName.objects.get(name=product.company_name)
    except:
        company = NewCompanyName.objects.create(name=product.company_name)
    Product.objects.create(name=product.name, company=company,details =product.details,buy_price=product.buy_price, sale_price=product.sale_price)
    return {200:'Success add new item'} 

@product_router.get("/", response=list[ProductResponseSchema],auth=AuthBearer())
def product_items(request):
    result=[]
    products=Product.objects.all()
    for product in products:
        result.append(
            {
                'id': str(product.id),
                'name' : product.name,
                'company_name' : product.company.name,
                'details' : product.details,
                'buy_price' : product.buy_price,
                'sale_price' : product.sale_price
            }
            
        )
    return result


@product_router.get("/{product_id}", response=ProductSchema,auth=AuthBearer())
def get_product(request, product_id: str):
    product = Product.objects.get(id=product_id)
    return {
                'name' : product.name,
                'company_name' : product.company.name,
                'details' : product.details,
                'buy_price' : product.buy_price,
                'sale_price' : product.sale_price
            }

@product_router.put("/{product_id}",auth=AuthBearer())
def update_product(request, product_id: str, product: ProductSchema):
    try:
        company = NewCompanyName.objects.get(name=product.company_name)
    except:
        company = NewCompanyName.objects.create(name=product.company_name)
    product_instance = Product.objects.get(id=product_id)
    product_instance.name = product.name
    product_instance.company = company
    product_instance.details = product.details
    product_instance.buy_price = product.buy_price
    product_instance.sale_price = product.sale_price
    product_instance.save()
    return {200:'Success edit item'} 

@product_router.delete("/{product_id}", response=dict,auth=AuthBearer())
def delete_product(request, product_id: str):
    product_instance = Product.objects.get(id=product_id)
    product_instance.delete()
    return {200: "Item deleted successfully"}
