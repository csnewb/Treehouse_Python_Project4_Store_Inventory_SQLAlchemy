import settings, utilities, db


def main_menu():
    while True:
        print(settings.main_menu)
        choice = utilities.force_letter("Choice: ", settings.main_menu_options).upper()
        if choice == "V":
            # View a single product's inventory
            db.get_single_item()
            pass
        elif choice == "A":
            # Add a new product to the database
            db.create_single_item()
            pass
        elif choice == "B":
            # Make a backup of the entire inventory
            db.create_backup()
            pass
        elif choice == "E":
            # Exit
            print("Exiting.... Goodbye")
            break
    exit()
