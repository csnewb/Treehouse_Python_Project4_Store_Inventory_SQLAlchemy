import random
from datetime import datetime

import db
import settings


def data_cleaner(row):
    if settings.DEBUG:
        print(f"processing: {row}")
    cleaned_data = {}
    product_name = row[0]

    try:
        product_price = row[1]
        product_price = product_price.split("$")[1]
        product_price = int(round(float(product_price), 2) * 100)

    except:
        print(f"  error converting product_price to int for {product_name}")
        product_price = row[1]

    try:
        product_quantity = int(row[2])
    except:
        print(f"  error converting product_quantity to int for {product_name}")
        product_quantity = row[2]

    try:
        date_updated = row[3]
        date_updated = datetime.strptime(date_updated, '%m/%d/%Y').date()
    except:
        print(f"  error converting date_updated to date for {product_name}")
        date_updated = row[3]

    cleaned_data['product_name'] = product_name
    cleaned_data['product_quantity'] = product_quantity
    cleaned_data['product_price'] = product_price
    cleaned_data['date_updated'] = date_updated


    return cleaned_data


def force_letter(prompt, valid_choices):
    while True:
        try:
            choice = str(input(prompt)).upper()
            valid_string = ', '.join(valid_choices)
            if choice in valid_choices:
                if settings.DEBUG:
                    print(f"Choice: {choice} in valid_choices: {valid_string}")
                return choice
        except:
            print(f"ERROR: Please choose one Letter: {valid_string}")
    return choice


def force_int_product_id(prompt, valid_choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_choices:
                break
        except:
            print(f"ERROR: Please choose a valid product ID")
    return choice


def get_valid_product_qty(prompt):
    while True:
        try:
            choice = int(input(prompt))
            if choice > 0:
                break
        except:
            print(f"ERROR: Please choose an integer greater than 0")
    return choice


def get_valid_product_name(prompt):
    while True:
        try:
            choice = input(prompt)
            name_available = db.check_if_name_available(choice)
            if name_available:
                return choice, False
            else:
                print(f"ERROR: That product name is currently in use.")
                new_prompt = "Would you like to update the record instead? Y for Yes, N for No: "
                options = ["Y", "N"]
                ask_update = force_letter(new_prompt, options).upper()
                if ask_update == "Y":
                    if settings.DEBUG:
                        print("Update Yes Selected, returning True")
                    return choice, True
                else:
                    print("Please choose a unique product_name")

        except:
            print(f"ERROR: Unknown exception with product_name. Please try again.")


def get_valid_product_price(prompt):
    while True:
        try:
            choice = float(input(prompt))
            if choice > 0:
                choice = round(choice * 100, 0)
                choice = int(choice)
                break
        except:
            print(f"ERROR: Please choose a valid float price greater than 0.00 DO NOT include the $")
    return choice


def get_unique_file_name():
    current_time = datetime.now()
    unique_id = current_time.strftime("%y-%m-%d-%H%M%S")
    fileprefix = "backup"
    fileext= ".csv"
    filename = fileprefix + unique_id + fileext
    return filename
