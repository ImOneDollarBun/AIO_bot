import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_detect(self, user_id):
        with self.connection:
            return self.cursor.execute("""INSERT  INTO 'users' (userid) VALUES (?)""",
                                       (user_id,))

    def user_if(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT userid FROM users WHERE userid = ?", (user_id,)).fetchone()

    def user_add(self, user_id, name, phone_num, age):
        with self.connection:
            return self.cursor.execute("UPDATE users SET phone_num = ?, name = ?, age = ? WHERE userid = ?",
                                       (phone_num, name, age, user_id,))

    def get_name(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT name FROM users WHERE userid = ?",
                                       (user_id,)).fetchone()[0]

    def get_age(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT age FROM users WHERE userid = ?",
                                       (user_id,)).fetchone()[0]

    def get_phone(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT phone_num FROM users WHERE userid = ?",
                                       (user_id,)).fetchone()[0]


class DataBaseItems:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def set_item(self, photo_num, name, description, price, who_added, catalog, photo_path):
        with self.connection:
            return self.cursor.execute("INSERT INTO items "
                                       "(photo_id, name, description, price, who_added, catalog, photo_path) "
                                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                       (photo_num, name, description, price, who_added, catalog, photo_path,))

    def get_item_id(self, photo_id):
        with self.connection:
            return self.cursor.execute("SELECT item_id FROM items WHERE photo_id = ?",
                                       (photo_id,)).fetchone()[0]

    def get_items_id(self):
        with self.connection:
            return [row[0] for row in self.cursor.execute("SELECT item_id FROM items").fetchall()]

    def id_exists(self, item_id):
        with self.connection:
            return self.cursor.execute("SELECT item_id FROM items WHERE item_id = ?",
                                       (item_id,)).fetchall()

    def get_item(self, item_id):
        with self.connection:
            return self.cursor.execute("SELECT "
                                       "photo_id, "
                                       "name, "
                                       "description, "
                                       "price,"
                                       "item_id, "
                                       "photo_path "
                                       "FROM items "
                                       "WHERE item_id = ?", (item_id,)).fetchall()[0]

    def get_photo_path(self, item_id):
        with self.connection:
            return self.cursor.execute("SELECT photo_path FROM items WHERE item_id = ?",
                                       (item_id,)).fetchone()[0]

    def get_item_by_catalog(self, catalog) -> list:
        with self.connection:
            return self.cursor.execute("SELECT item_id FROM items WHERE catalog = ?",
                                       (catalog,)).fetchall()

    def get_catalog_by_item(self, item_id):
        with self.connection:
            return self.cursor.execute("SELECT catalog FROM items WHERE item_id = ?",
                                       (item_id,)).fetchall()

    def delete_item(self, item_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))


class SYS:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def change_quality(self, count):
        with self.connection:
            return self.cursor.execute("UPDATE sys SET img_quality = ?", (count,))

    def get_quality(self):
        with self.connection:
            return self.cursor.execute("SELECT img_quality FROM sys").fetchone()[0]


class CatalogName:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_names(self):
        with self.connection:
            return [row[0] for row in self.cursor.execute("SELECT name, num_name FROM catalog_names").fetchall()]

    def set_names(self, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO catalog_names (name) VALUES (?)", (name,))

    def delete_names(self, name_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM catalog_names WHERE num_name = ?", (name_id,))

    def get_id_by_name(self, name) -> tuple:
        with self.connection:
            return self.cursor.execute("SELECT num_name FROM catalog_names WHERE name = ?",
                                       (name,)).fetchone()

    def name_exists(self, name):
        with self.connection:
            try:
                return len(self.cursor.execute("SELECT * FROM catalog_names WHERE name = ?",
                                               (name,)).fetchone()[0]) == 1
            except:
                return False


class CartUsage:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def set_items(self, items, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO cart (items_list, who_offer) VALUES (?, ?)",
                                       (items, user_id,))

    def update_items(self, items, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE cart SET items_list = ? WHERE who_offer = ?",
                                       (items, user_id,))

    def get_items(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT items_list FROM cart WHERE who_offer = ?",
                                       (user_id,)).fetchone()

    def item_exists(self, user_id):
        with self.connection:
            try:
                return self.cursor.execute("SELECT items_list FROM cart WHERE who_offer = ?",
                                           (user_id,)).fetchone()[0]
            except:
                return False
