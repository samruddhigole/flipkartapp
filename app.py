from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_serialize import FlaskSerializeMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://flipkartuser:admin123@localhost:5432/flipkartapp"
db = SQLAlchemy(app)
migrate = Migrate(app,db)
FlaskSerializeMixin.db = db


@app.route("/home",methods=["GET"])
def home():
    return {"result":"FLIPKART APP"}

@app.route("/createProduct",methods=["POST"])
def create_product():
    if request.method == 'POST':
        product = request.get_json()
        print(product)
        product_name = product["product_name"]
        product_price = product["product_price"]
        product_quantity = product["product_quantity"]
        product_details = product["product_details"]
        new_product = Product(product_name=product_name,product_price=product_price,product_quantity=product_quantity,product_details=product_details)
        db.session.add(new_product)
        db.session.commit()
    return{"result":"New Product is created"}


@app.route("/getProduct",methods=["GET"])
def get_product_details():
    products = Product.query.all()
    result = [
            {
                "pid":product.id,
                "product_name":product.product_name,
                "product_price":product.product_price,
                "product_quantity":product.product_quantity,
                "product_details":product.product_details
                }
            for product in products]
    return {"result":result}

@app.route("/getProduct/<int:id>",methods=["GET"])
def get_product_byid(id):
    product = Product.query.get_or_404(id)
    result = {
                "pid":product.id,
                "product_name":product.product_name,
                "product_price":product.product_price,
                "product_quantity":product.product_quantity,
                "product_details":product.product_details
            }
    return{"result":result}


@app.route("/createCustomer",methods=["POST"])
def create_customer():
    if request.method == 'POST':
        customer = request.get_json()
        print("kjhk",customer)
        customer_name = customer["customer_name"]
        customer_email = customer["customer_email"]
        customre_passwd = customer["customer_passwd"]
        new_customer = Customer(customer_name=customer_name,customer_email=customer_email,customre_passwd=customre_passwd)
        db.session.add(new_customer)
        db.session.commit()
    return{"result":"customer is created"},201

@app.route("/getCustomer",methods=["GET"])
def get_customer():
    print("in get customer")
    customers = Customer.query.all()
    print(customers)
    result = [
            {
                "cid":customer.id,
                "customer_name":customer.customer_name,
                "customer_email":customer.customer_email,
                "customer_passwd":customer.customre_passwd
                }
            for customer in customers]
    return{"customers":result}

@app.route("/getCustomer/<int:id>",methods=["GET"])
def get_customer_byid(id):
    customer = Customer.query.get_or_404(id)
    result = {
            "cid":customer.id,
            "customer_name":customer.customer_name,
            "customer_email":customer.customer_email
            }
    return{"customer":result}



class Customer(FlaskSerializeMixin,db.Model):
    __tablename__ = 'customer_detail_table'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    customer_email = db.Column(db.String)
    customre_passwd = db.Column(db.String)

    serialize_only=('customer_name','customer_email','customre_passwd')
    create_fields = update_fields = ['customer_name','customer_email','customre_passwd']

    def __init__(self,customer_name,customer_email,customre_passwd):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customre_passwd = customre_passwd

class Product(FlaskSerializeMixin,db.Model):
    __tablename__ = 'product_detail'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_price = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    product_details = db.Column(db.String)

    serialize_only=('product_name','product_price','product_quantity','product_details')
    create_fields = update_fields = ['product_name','product_price','product_quantity','product_details']

    def __init__(self,product_name,product_price,product_quantity,product_details):
        self.product_name = product_name
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_details = product_details


db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)



