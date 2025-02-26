from flask import jsonify, request, abort
from service import app
from service.models import Product
from service.common import status

######################################################################
# INDEX ROUTE
######################################################################
@app.route("/")
def index():
    return jsonify(message="Product Catalog Administration"), status.HTTP_200_OK

######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health():
    return jsonify(message="OK"), status.HTTP_200_OK

######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")

    product = Product()
    product.deserialize(request.get_json())
    product.create()

    location_url = f"{BASE_URL}/{product.id}"
    return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# RETRIEVE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single Product
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return product.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update a Product
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

    product.deserialize(request.get_json())
    product.update()
    return product.serialize(), status.HTTP_200_OK

######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a Product
    """
    app.logger.info("Request to Delete a product with id [%s]", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    
    return "", status.HTTP_204_NO_CONTENT

######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns a list of Products"""
    app.logger.info("Request to list Products...")
    
    products = Product.all()
    results = [product.serialize() for product in products]

    app.logger.info("[%s] Products returned", len(results))
    return results, status.HTTP_200_OK
