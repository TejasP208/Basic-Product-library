from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from database import engine
import database_models
from models import Product
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



products=[
     Product(id=1,name="Phone",description="budget phone",price=4500,quantity=4),
     Product(id=2,name="laptop",description="budget laptop",price=45000,quantity=9),
     Product(id=5,name="Tablet",description="costly tablet",price=4000,quantity=3),
     Product(id=8,name="Smart_watch",description="best smart_watch",price=2000,quantity=4),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def __init__db():
    db = SessionLocal()
    count = db.query(database_models.Product)
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()
__init__db()

@app.get("/products")
def get_all_products(db:Session =Depends(get_db)):
     db_products = db.query(database_models.Product).all()
     return db_products

@app.get("/products/{id}")
def get_product(id:int ,db:Session =Depends(get_db) ):
     db_products = db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if  db_products:
        return db_products
    
     return "Product not found"

@app.post("/products/{id}")
def add_product(product:Product , db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_products:
            db_products.name= product.name
            db_products.description= product.description
            db_products.price= product.price
            db_products.quantity= product.quantity
            db.commit()
            return "Product updated successfully"
    return "Product not found"


@app.delete("/products/{id}")
def delete_product(id:int , db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "product deleted sucessfully"
    return "product not found"