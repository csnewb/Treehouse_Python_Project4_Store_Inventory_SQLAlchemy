import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import csv

import utilities, settings
from models import Products

engine = create_engine('sqlite:///inventory.db')
Session = sessionmaker(bind=engine)
session = Session()

def import_from_csv_to_db():
    with open("store-inventory/inventory.csv", "r") as file:
        for row in file:
            print(row)


def import_from_csv_to_db():
    with open("store-inventory/inventory.csv", "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:

            cleaned_data = utilities.data_cleaner(row)

            product_exists = session.query(Products).filter(Products.product_name == cleaned_data['product_name']).first()
            if product_exists:
                if settings.DEBUG:
                    print(f"    product exists: {product_exists.product_name}")
                if product_exists.date_updated < cleaned_data['date_updated']:
                    if settings.DEBUG:
                        print(f"    product_exists.date_updated: {product_exists.date_updated} < {cleaned_data['date_updated']}")
                    # Update the existing product with the new data
                    product_exists.product_quantity = cleaned_data['product_quantity']
                    product_exists.product_price = cleaned_data['product_price']
                    product_exists.date_updated = cleaned_data['date_updated']
                else:
                    if settings.DEBUG:
                        print(f"    Product information is in database and more current, import of item cancelled - {cleaned_data['product_name']}")
                    continue
            else:
                if settings.DEBUG:
                    print(f"    Product not in database, good to upload: {cleaned_data['product_name']}")

            product = Products(
                product_name=cleaned_data['product_name'],
                product_quantity=cleaned_data['product_quantity'],
                product_price=cleaned_data['product_price'],
                date_updated=cleaned_data['date_updated']
            )

            session.add(product)

    if settings.DEBUG:
        new_products = session.new
        for np in new_products:
            print(np.product_name)
        if len(new_products) < 1:
            print(f"*** NO NEW ITEMS ADDED ***")
    session.commit()
    session.close()

    if settings.DEBUG:
        len_query = max(get_product_ids())
        print(f"The Newest Item in the Database is product_id: {len_query}")

def get_product_ids():
    """
    The purpose of this function is to return a list of all currently valid product_ids
    :return: list(product_ids)
    """
    product_ids = []
    for product in session.query(Products):
        product_ids.append(product.product_id)
    session.close()

    return product_ids

def get_single_item():
    print(f"\n---------- View Single Item -----------")
    valid_choices = get_product_ids()
    choice = utilities.force_int_product_id("Which Product ID? ", valid_choices)
    query = session.query(Products).filter_by(product_id=choice).first()
    print_statement = f"""
    Product Name: {query.product_name}
    Product ID: {query.product_id}
    Product Qty: {query.product_quantity}
    Product Price: ${query.product_price/100}
    Last Updated: {query.date_updated}
    """
    print(print_statement)
    session.close()

def check_if_name_available(product_name):
    query = session.query(Products).filter_by(product_name=product_name).first()
    if query:
        # product found in inventory
        session.close()
        return False
    else:
        # product not found in inventory
        session.close()
        return True


def create_single_item():
    print(f"\n---------- Create New Item -----------")
    product_name, update = utilities.get_valid_product_name("product name: ")
    product_price = utilities.get_valid_product_price("product price: ")
    product_qty = utilities.get_valid_product_qty("product qty: ")
    product_updated = datetime.date.today()

    if update:
        if settings.DEBUG:
            print(f"Update chosen as Yes")
        query = session.query(Products).filter_by(product_name=product_name).first()
        query.product_price = product_price
        query.product_quantity = product_qty
        query.date_updated = product_updated
        try:
            session.commit()
            print(f"Product Successfully updated: Product ID: {query.product_id}")
        except:
            print(f"Error trying to update product - {product_name}")

    else:
        product = Products(
            product_name=product_name,
            product_quantity=product_qty,
            product_price=product_price,
            date_updated=product_updated
        )
        try:
            session.add(product)
            session.commit()
            print(f"Product Successfully added: Product ID: {product.product_id}")
        except:
            print(f"Error trying to add product - {product_name}")
    session.close()


def create_backup():
    print(f"Creating a Backup of Database")
    filename = utilities.get_unique_file_name()
    print(f"--{filename}")

    product_list = []
    for product in session.query(Products):
        row = [product.product_id,
               product.product_name,
               product.product_quantity,
               product.product_price,
               product.date_updated
               ]
        product_list.append(row)

    with open(filename, 'w', newline='') as backup_file:
        writer = csv.writer(backup_file)
        writer.writerow(Products.__table__.columns.keys())
        for row in product_list:
            writer.writerow(list(row))

    print(f"Backup File Created with {len(product_list)} products")
