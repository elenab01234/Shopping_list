from db import engine, Session, Base,ShoppingListItem, ShoppingListCategory


class ShoppingListDb:
    @staticmethod
    def save_items(data_df):
        data_df.to_sql("shoppinglistitemtable", engine, if_exists="replace", index=True)


    @staticmethod
    def get_all_categories():
        with Session() as session:
            categories = session.query(ShoppingListCategory).all()
            if categories != []:
                return categories
            category_options = [
                "Fruits",
                "Vegetables",
                "Dairy",
                "Bread & Bakery",
                "Meat & Fish",
                "Cans & Jars",
                "Pasta, Rice & Cereal",
                "Sauces, Condiments & Spices",
                "Frozen Foods",
                "Snacks",
                "Drinks",
                "Household & Cleaning",
                "Personal Care",
                "Pet Care",
                "Baby Items"
            ]
            for categ in category_options:
                new_ShoppingCategory = ShoppingListCategory(Category=categ)
                session.add(new_ShoppingCategory)
            return session.query(ShoppingListCategory).all()

    @staticmethod
    def get_all_items():
        with Session() as session:
            items = session.query(ShoppingListItem).all()
            return items

