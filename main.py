import psycopg2


def create_db(conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL);
        
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES client(id),
        phone VARCHAR(15) UNIQUE);''')


def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute('''
        INSERT INTO client (first_name, last_name, email) 
        VALUES (%s, %s, %s) RETURNING id''', (first_name, last_name, email))

    client_id = cur.fetchone()[0]

    cur.execute('''
    INSERT INTO phones (client_id, phone) 
    VALUES (%s, %s)''', (client_id, phone))


def add_phone(conn, client_id, phone):
    cur.execute('''
        INSERT INTO phones(client_id, phone)
        VALUES (%s, %s)''', (client_id, phone))


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
        UPDATE client 
        SET first_name = %s, last_name = %s, email = %s
        WHERE id = %s;''', (first_name, last_name, email, client_id))

    cur.execute('''
        UPDATE phones SET phone = %s WHERE client_id = %s;
        ''', (phone, client_id))



def delete_phone(conn, client_id, phone):
    cur.execute('''
        DELETE FROM phones WHERE client_id = %s OR phone = %s''', (client_id, phone))


def delete_client(conn, client_id):
    cur.execute('''
            DELETE FROM phones WHERE client_id = %s''', (client_id,))

    cur.execute('''
        DELETE FROM client WHERE id = %s''', (client_id,))




def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
        SELECT first_name, last_name FROM client
        JOIN phones ON client.id = phones.client_id
        WHERE first_name iLIKE %s OR last_name iLIKE %s 
        OR email iLIKE %s OR phone iLIKE %s
        GROUP BY first_name, last_name;''', (first_name, last_name, email, phone))


    result = cur.fetchone()
    string = ' '.join(result)
    print(string)




with psycopg2.connect(database="client_db", user="postgres", password="1604") as conn:
    with conn.cursor() as cur:
        conn.autocommit = True
        # create_db(conn)
        # add_client(conn, 'Владимир', 'Вологодский', 'ss@koa.ru', '11111111111')   # 1-я Функция
        # add_client(conn, 'Владислав', 'Матроскин', 'vlad@glad.com', '22222222222')   # 1-я Функция
        # add_client(conn, 'Витя', 'Иванов', 'ssdfgha@koa.ru', '333333333333')   # 1-я Функция
        # add_client(conn, 'Вася', 'Шуткович', 'qaerhg@koa.ru') # 1-я Функция
        # add_phone(conn, 1, '879862135')   # 3-я Функция
        # add_phone(conn, 3, '13456687')   # 3-я Функция
        # change_client(conn, 1, 'Анатолий', 'Анатольев', 'adsfb@koa.ru', '987654321')   # 4-я Функция
        # delete_phone(conn, None, '11111111111') # 5-я Функция
        # delete_client(conn, 4)   # 6-я Функция
        # find_client(conn, None, None, None, '22222222222') # 7-я Функция
        # find_client(conn, None, None, 'ss@koa.ru', None) # 7-я Функция
conn.close()
