import sqlite3 as sq
import csv



DATABASE = 'products.db'
CSV_PATH = '/home/user/Desktop/Furniture_project/Products_import.xlsx'


con = sq.connect(DATABASE)

cur = con.cursor()



cur.execute('''CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY,
    product_type TEXT NOT NULL,
    product_name TEXT NOT NULL,
    article TEXT UNIQUE,
    min_partner_cost DECIMAL(10,2),
    material_type TEXT NOT NULL
)''')


cur.execute('''CREATE TABLE IF NOT EXISTS product_coefficient (
    id INTEGER PRIMARY KEY,
    product_id INTEGER UNIQUE,
    coefficient DECIMAL(5,3) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS lose_coefficient (
    id INTEGER PRIMARY KEY,
    material_type TEXT UNIQUE,
    lose_percentage DECIMAL(5,2) NOT NULL
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS department_work_time (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    department_name TEXT NOT NULL,
    production_time DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
)''')


cur.execute('''CREATE TABLE IF NOT EXISTS department (
    id INTEGER PRIMARY KEY,
    department_name TEXT UNIQUE,
    department_type TEXT NOT NULL
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS department_workers (
    id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    workers_count INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id)
)''')



con.commit()
con.close()