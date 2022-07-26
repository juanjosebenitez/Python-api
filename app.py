from email import message
from flask import Flask,jsonify,request
from flask_wtf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

from products import products

product_not_found_message="Product not Found!"

@app.route("/products")
def get_products():
    return jsonify(products)

@app.route("/products/<string:product_name>")
def get_product(product_name):
    products_found = [product for product in products if product['name']==product_name]

    if (len(products_found)>0):
        return jsonify(products_found[0])

    return jsonify({"message":product_not_found_message})
    
@app.route("/products", methods=['POST'])
def add_product():
    new_product = {
        "name":request.json['name'],
        "price":request.json['price'],
        "quantity":request.json['quantity']
    }

    products.append(new_product)
    return jsonify({"message":"Product added","products":products})

@app.route("/products/<string:product_name>", methods=['PUT'])
def edit_product(product_name):
    products_found = [product for product in products if product['name']==product_name]

    if (len(products_found)>0):
        products_found[0]['name']=request.json['name']
        products_found[0]['price']=request.json['price']
        products_found[0]['quantity']=request.json['quantity']
        return jsonify({"messge":"Product updated","products":products})
    return jsonify({"message":product_not_found_message})

@app.route("/products/<string:product_name>", methods=['DELETE'])
def delete_product(product_name):
    products_found = [product for product in products if product['name']==product_name]

    if (len(products_found)>0):        
        products.remove(products_found[0])
        return jsonify({"messge":"Product deleted","products":products} )
    return jsonify({"message":product_not_found_message})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
