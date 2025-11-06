#!/usr/bin/env python3
import sqlite3
import os

db_path = 'data/products.db'
print(f'DB exists: {os.path.exists(db_path)}')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM products')
    print(f'Products count: {cursor.fetchone()[0]}')
    cursor.execute('SELECT name, product_id, price, ean, image_url FROM products LIMIT 10')
    products = cursor.fetchall()
    print('\nProducts in database:')
    for i, p in enumerate(products, 1):
        print(f'  {i}. {p[0][:60]}')
        print(f'      ID: {p[1]}, Price: {p[2]}€, EAN: {p[3]}, Image: {"Yes" if p[4] else "No"}')
    conn.close()
