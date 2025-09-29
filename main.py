from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
     db.close()

def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump())) # unpacking, ** gives key value pairs from dict
    
        db.commit() # we disabled this by default earlier

init_db()

# endpoints

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):

    # OLD: return products

    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    '''
    OLD:
    for product in products:
        if product.id == id:
            return product
    return "product not found"
    '''
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found bro!"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    '''OLD:
    products.append(product)
    return product # returns what you added, pythonic!
    '''
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product # returns what you added, pythonic!


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    '''OLD:
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product added successfully!"
        
    return "No such product found!"
    '''

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated!"
    else:
        return "No product found!"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    '''OLD:
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product successfully removed!"

    return "The product that you want to delete was not found!"
    '''

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product successfully deleted!"
    else:
        return "Product not found!"
