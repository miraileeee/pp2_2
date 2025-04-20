import psycopg2
import os, csv
from config import load_config

def create(cur):
    cur.execute(
                """CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    phone TEXT);"""
            )
    print('Table created successfully')

def insert(cur):
    name = input('Contact name: ')
    phone = input('Phone number: ')
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES(%s, %s)", (name, phone)
    )
    print('Inserted successfully')

def insert_csv(cur):
    path = input('File path: ')
    with open(path, 'r') as f:
        next(f)
        cur.copy_expert(
            "COPY phonebook (name, phone) FROM stdin WITH CSV HEADER", f
        )
    print('Copied successfully')

def insert_many(cur):
    names = input('Contact names: ').split()
    phones = input('Contact phones: ').split()

    if len(names) != len(phones):
        print('The number of names and phones does not match')
        return
    
    invalid = []

    for i in range(len(names)):
        n = names[i]
        p = phones[i]

        if p.isdigit() and len(p) == 11:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (n, p)
            )
        else:
            invalid.append((n, p))
        
    if invalid:
        print('Please check the data you have entered')
        for n, p in invalid:
            print(f"Name: {n}, Phone: {p}")
        insert_many(cur)    

    else:
        print('Inserted successfully')

def update(cur):
    upd_name = input('Updated contact name: ')
    upd_phone = input('Updated phone number: ')
    cur.execute(
        "UPDATE phonebook SET name = %s WHERE phone = %s", (upd_name, upd_phone)
    )
    print('Updated successfully')

def delete(cur):
    inp = input('Choose what to delete (name/phone): ')
    if inp == 'name': 
        name = input('Contact name to delete: ')
        cur.execute(
        "DELETE FROM phonebook WHERE  name = %s", (name,)
        )
        print('Deleted successfully')

    if inp == 'phone':
        phone = input('Phone number to delete: ')
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s", (phone,)
        )
        print('Deleted successfully')

def query(cur):
    filter = input('Filter by (name/phone): ')

    if filter == 'name':
        name = input('Contact name to search for: ').strip()
        search = f"%{name}%"
        cur.execute(
            "SELECT * FROM phonebook WHERE name ILIKE %s", (search,)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)
    
    if filter == 'phone':
        phone = input('Phone number starting with: ').strip()
        search = f"%{phone}%"
        cur.execute(
            "SELECT * FROM phonebook WHERE phone ILIKE %s", (search,)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)

def query_page(cur):
    limit = int(input('Number of contacts to display: '))
    offset = int(input('Number of contacts to skip: '))

    cur.execute(
        "SELECT name, phone FROM phonebook LIMIT %s OFFSET %s", (limit, offset)
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)

def editor():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            cur = conn.cursor()
            create(cur)
            print("Operations: input from console/input from csv/input several contacts/update/delete/query/query a page/exit")
            
            while True:
                inp = input("Choose an operation: ")
                    
                if inp == 'input from console':
                    insert(cur)
                elif inp == 'input from csv':
                    insert_csv(cur)
                elif inp == 'input several contacts':
                    insert_many(cur)
                elif inp == 'update':
                    update(cur)
                elif inp == 'delete':
                    delete(cur)
                elif inp == 'query':
                    query(cur)
                elif inp == 'query a page':
                    query_page(cur)
                elif inp == 'exit':
                    break
                    
                conn.commit()

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    
    finally:
        if cur:
            cur.close()

if __name__ == '__main__':
    editor()

