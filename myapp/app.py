from flask import Flask, jsonify, request
from products import products
app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"message":"Pong!"})

@app.route("/products", methods=["GET"])
def getProducts():
    return jsonify({"products": products})

@app.route("/products/<string:product_name>")
def getProduct(product_name):
    print(product_name)
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        return jsonify({"product": productFound[0]})
    return jsonify({"message": "Not Found"})

@app.route('/products', methods=['POST'])
def addProduct():
    print(request.json)
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message":"Product Added Successfully","products":products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]

    if(len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({"message": "Product Updated Successfully", "product":productFound[0]})

    return jsonify({"message":"Product Not Found"})

@app.route('/product/<string:product_name>',methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]

    if (len(productsFound) > 0):
        products.remove(productsFound[0])
        return jsonify({"message":"Product Deleted Successfully","products":products})
    
    return jsonify({"message":"Product Not Found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)