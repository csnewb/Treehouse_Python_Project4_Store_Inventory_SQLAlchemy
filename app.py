

import models, db, settings, utilities, menu



if __name__ == "__main__":
    models.Base.metadata.create_all(bind=db.engine)
    db.import_from_csv_to_db()
    if settings.DEBUG:
        print(settings.debug_warning)
    print(settings.Greeting)
    menu.main_menu()
