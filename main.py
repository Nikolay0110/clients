import psycopg2


def create_db(conn):
    # Здесь создать базу данных

    cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL);
        ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS phone_number(
        id SERIAL PRIMARY KEY,
        number VARCHAR(50) UNIQUE,
        client_id INTEGER REFERENCES client(id));
        ''')


def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute('''
        INSERT INTO client (first_name, last_name, email)
        VALUES (%S, %S, %S) RETURNING id;''', (first_name, last_name, email))


def add_phone(conn, client_id, phone):
    cur.execute('''
        INSERT INTO phone (client_id, phone)
        VALUES (%S, %S);''', (client_id, phone))


#
# def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
#     pass
#
#
# def delete_phone(conn, client_id, phone):
#     pass
#
#
# def delete_client(conn, client_id):
#     pass
#
#
# def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
#     pass
#
#
with psycopg2.connect(database="client_db", user="postgres", password="1604") as conn:
    with conn.cursor() as cur:
        conn.autocommit = True
        create_db(conn)
        sql = 'CREATE DATABASE client'
conn.close()
