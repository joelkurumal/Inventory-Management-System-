import sqlite3

conn = sqlite3.connect("inventory management system.db")
cursor = conn.cursor()

# ----------------create table---------------- #

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER,
    price REAL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()

# ---------------- registration ---------------- #

current_user_id = None

def register():
    u = input("Enter Username: ")
    p = input("Enter Password: ")

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (u, p)
        )
        conn.commit()
        print("Registration Successful!")
    except sqlite3.IntegrityError:
        print("Username already exists!")

# ---------------- login ---------------- #
def login():
    global current_user_id

    u = input("Enter Username: ")
    p = input("Enter Password: ")

    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (u, p)
    )

    result = cursor.fetchone()

    if result:
        current_user_id = result[0]
        print("Login Successful!")
        inventory_menu()
    else:
        print("Invalid Username or Password")

# ---------------- add product---------------- #

def add_product():
    try:
        name = input("Enter Product Name: ")
        quantity = int(input("Enter Quantity: "))
        price = float(input("Enter Price: "))

        cursor.execute(
            "INSERT INTO products(name, quantity, price, user_id) VALUES(?, ?, ?, ?)",
            (name, quantity, price, current_user_id)
        )
        conn.commit()

        print("Product Added Successfully!")
    except:
        print("Invalid input! Please enter correct values.")

# ----------------view product ---------------- #
def view_products():
    cursor.execute(
        "SELECT product_id, name, quantity, price FROM products WHERE user_id=?",
        (current_user_id,)
    )

    products = cursor.fetchall()

    print("\nID\tName\tQuantity\tPrice")
    print("-----------------------------------------")

    for p in products:
        print(p[0], "\t", p[1], "\t", p[2], "\t\t", p[3])

# ---------------- update product ---------------- #
def update_product():
    try:
        pid = int(input("Enter Product ID: "))
        quantity = int(input("Enter New Quantity: "))
        price = float(input("Enter New Price: "))

        cursor.execute(
            "UPDATE products SET quantity=?, price=? WHERE product_id=? AND user_id=?",
            (quantity, price, pid, current_user_id)
        )
        conn.commit()

        print("Product Updated Successfully!")
    except:
        print("Invalid input!")

# ---------------- delete product ---------------- #
def delete_product():
    try:
        pid = int(input("Enter Product ID: "))

        cursor.execute(
            "DELETE FROM products WHERE product_id=? AND user_id=?",
            (pid, current_user_id)
        )
        conn.commit()

        print("Product Deleted Successfully!")
    except:
        print("Invalid input!")

# ----------------search product ---------------- #
def search_product():
    name = input("Enter Product Name: ")

    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ? AND user_id=?",
        ('%' + name + '%', current_user_id)
    )

    products = cursor.fetchall()

    if products:
        print("\nID\tName\tQuantity\tPrice")
        print("-----------------------------------------")
        for p in products:
            print(p[0], "\t", p[1], "\t", p[2], "\t\t", p[3])
    else:
        print("Product Not Found!")

# ---------------- MENU ---------------- #

def inventory_menu():
    while True:
        print("\n===== INVENTORY MENU =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            print("Logged Out Successfully!")
            break
        else:
            print("Invalid Choice!")

# ---------------- MAIN ---------------- #

while True:
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        print("Thank You!")
        break
    else:
        print("Invalid Choice!")

conn.close()
