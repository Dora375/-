import tkinter as tk
import sqlite3


class InventorySystem:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_categories(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''SELECT * FROM categories;''')

        categories = []


        for category in cursor.fetchall():
            print(category)
            categories.append(Category(category[0], category[1]))
        return categories

    def get_products_amount(self, category_id):
        cursor = self.db_connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM products WHERE category_id = ?''', category_id)
        return cursor.fetchall()

    def get_category_by_name(self, name):
        for category in self.get_categories():
            if name == category.name:
                return category

    def get_category(self):
        pass


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Interface:
    def __init__(self, master, inventory_system):
        self.category_frame = None
        self.current_item_info = None
        self.current_item_label = None
        self.main_frame = None
        self.left_frame = None
        self.inventory_listbox = None
        self.inventory_system = inventory_system
        self.master = master
        self.master.title("Система автоматизації складу")
        self.master.geometry("600x400")  # Задаємо розміри вікна (ширина x висота)

        self.create_widgets()

    def show_home_page(self):
        # Повертаємося на головну сторінку
        # Очищаємо вміст фрейму для товарів
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Відображаємо повідомлення про оберіть категорію
        self.product_info_label = tk.Label(self.products_frame, text="Оберіть категорію для перегляду товарів")
        self.product_info_label.pack()

        # Показуємо кнопку для повернення на головну сторінку
        self.back_to_home_button = tk.Button(self.products_frame, text="На головну", command=self.show_home_page)
        self.back_to_home_button.pack()

    def create_widgets(self):
        # Основний фрейм
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для категорій
        self.categories_frame = tk.Frame(self.main_frame, width=200)
        self.categories_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Фрейм для інформації про товари
        self.products_frame = tk.Frame(self.main_frame)
        self.products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Listbox для відображення категорій
        self.categories_listbox = tk.Listbox(self.categories_frame)
        self.categories_listbox.pack(fill=tk.BOTH, expand=True)
        self.categories_listbox.bind("<<ListboxSelect>>", self.show_category_details)

        # Кнопка для створення нової категорії
        self.new_category_button = tk.Button(self.categories_frame, text="Створити категорію",
                                             command=self.create_new_category)
        self.new_category_button.pack()

        # Додаткові віджети для відображення інформації про товари та їх деталей
        self.product_info_label = tk.Label(self.products_frame, text="Оберіть категорію для перегляду товарів")
        self.product_info_label.pack()

        self.back_to_home_button = tk.Button(self.products_frame, text="На головну", command=self.show_home_page)
        self.back_to_home_button.pack()

        # for category in categories:
        #     self.inventory_listbox.insert(tk.END, category.id)
        # self.inventory_listbox.bind("<<ListboxSelect>>", self.show_item_details)

    def create_new_category(self):
        # Метод для створення нової категорії
        pass

    def edit_product(self):
        # Метод для редагування товару
        pass

    def delete_product(self):
        # Метод для видалення товару
        pass
    def show_category_details(self, event):
        # Очищаємо вміст фрейму для товарів
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Отримуємо індекс вибраної категорії
        selected_index = self.categories_listbox.curselection()
        if not selected_index:
            return

        # Отримуємо інформацію про категорію
        category_id = selected_index[0]  # Припустимо, що індекси в Listbox відповідають ідентифікаторам категорій
        category_name = self.categories_listbox.get(category_id)

        # Відображаємо інформацію про категорію та її товари
        tk.Label(self.products_frame, text=f"Категорія: {category_name}").pack()

        # TODO: Відображення списку товарів у вибраній категорії
        # Замість цього, ви можете використовувати ваш метод для відображення списку товарів

        # Додаткові віджети та кнопки для редагування та видалення товарів
        edit_button = tk.Button(self.products_frame, text="Редагувати товар", command=self.edit_product)
        edit_button.pack()

        delete_button = tk.Button(self.products_frame, text="Видалити товар", command=self.delete_product)
        delete_button.pack()

    def show_item_details(self, event):
        self.main_frame.pack_forget()

        category_name = self.inventory_listbox.get(self.inventory_listbox.curselection())
        category = self.inventory_system.get_category_by_name(category_name)

        self.category_frame = tk.Frame(self.master)
        self.category_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        current_item_label = tk.Label(self.category_frame, text="Ви обрали категорію: " + category.name)
        current_item_label.pack(pady=5)

        products_amount = self.inventory_system.get_products_amount()

        tk.Label(self.category_frame,
                 text="Кількість товарів у категорії складає: " + products_amount + " позицій").pack()

        # quantity = self.inventory[selected_item]["Кількість"]
        # description = self.inventory[selected_item]["Опис"]
        # self.current_item_info.config(text=f"Кількість: {quantity}\nОпис: {description}")


def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name VARCHAR(255))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name VARCHAR(255), description 
    TEXT, category_id INTEGER, quantity INTEGER, FOREIGN KEY(category_id) REFERENCES categories(id))''')

    cursor.execute('''INSERT INTO categories (name) VALUES ('Test')''')
    cursor.execute('''INSERT INTO products (name, description, quantity, category_id) VALUES (?, ?, ?, ?)''', ("test", "test", 10, 1))
    cursor.execute('''INSERT INTO products (name, description, quantity, category_id) VALUES (?, ?, ?, ?)''', ("test2", "test2", 1, 1))

    root = tk.Tk()
    inventory_system = InventorySystem(conn)
    ui = Interface(root, inventory_system)
    root.mainloop()


if __name__ == "__main__":
    main()
