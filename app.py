from math import prod
from urllib import response
from xml.dom import NotFoundErr
from flask import Flask, jsonify, redirect, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from product import Product
import product

db = dbase.dbConnection() #Conexion a la base de datos


app = Flask(__name__) # instanciar

#Ruta principal
@app.route('/')
def home(): #Función de la rutaa
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products = productsReceived)


#Metodo post, para crear datos
@app.route('/products', methods=['POST']) #Función de la ruta
def addProduct():
    products = db['products'] #coleccion de la base de datos
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection)
        response = jsonify({
            'name ': name,
            'price': price,
            'quantity': quantity
        })
        return redirect(url_for('home'))
    else:
        return NotFound()
    

#Metodo delete, para eliminar
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

#Metodo put, para editar
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products'] #coleccion de la base de datos
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        responde = jsonify({ 'message' : 'Producto' + product_name + 'actualizado'})
        return redirect(url_for('home'))
    else:
        return NotFound()

@app.errorhandler(404)
def NotFound(error=None):
    message = {
        'message' : 'No encontrado '+ request.url,
        'status' : '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(debug=True, port=4000) #para lanzar el archivo en el puerto establecido 4000
