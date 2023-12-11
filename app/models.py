import sqlite3 as sql
from datetime import datetime

def checklogin():
    con = sql.connect("rcart.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
   
    con.commit()
    con.close()
    return users

def tag_exist(tag_id):
    con = sql.connect("rcart.db")
    cur = con.cursor()
    cur.execute("SELECT tag_id FROM products")
    records = cur.fetchall()

    for row in records:  #records here is a list of tuples
        if tag_id == row[0]: 
            con.commit()
            con.close()
            return False

    con.commit()
    con.close()
    return True  

def add_tags(tag_id, name):
    con = sql.connect("rcart.db")
    cur = con.cursor()
    cur.execute("INSERT INTO products(tag_id, product_name) VALUES (?,?)", (tag_id, name))
    con.commit()
    con.close()

def get_all_uids():
    con = sql.connect("rcart.db")
    cur = con.cursor()
    #get the latest data
    cur.execute("SELECT tag_id FROM products")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def get_products_data():
    con = sql.connect("rcart.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def update_uid(id):
    value = f"{id}"
    query = f"UPDATE products SET quantity = quantity + 1 WHERE tag_id = '{value}'"
    con = sql.connect("rcart.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()

def delete_product_data(id):
    value = f"{id}"
    con = sql.connect("rcart.db")
    cur = con.cursor()
    query = f"DELETE FROM products WHERE tag_id = '{value}'"
    cur.execute(query)
    con.commit()
    con.close()

