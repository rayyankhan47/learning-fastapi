from fastapi import FastAPI
from models import Product
from database import SessionLocal, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to my packaging app!"

products = [
    Product(id=1, name="phone", description="cool phone", price=100.00, quantity=10),
    Product(id=2, name="laptop", description="nice laptop", price=499.99, quantity=8),
    Product(id=3, name="pen", description="great pen", price=11.99, quantity=3),
    Product(id=4, name="book", description="interesting book", price=15.00, quantity=20),
]



@app.get("/products")
def get_all_products():
    # db connection
    db = SessionLocal()
    # query
    db.query
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "product not found"

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product added successfully!"
        
    return "No such product found!"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product successfully removed!"

    return "The product that you want to delete was not found!"