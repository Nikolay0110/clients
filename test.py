import psycopg2

def add_new_user(first_name, last_name, email, phone_numbers=None):
    try:
        conn = psycopg2.connect(database="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")
        cur = conn.cursor()
        cur.execute("INSERT INTO client (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id", (first_name, last_name, email))
        client_id = cur.fetchone()[0]  # получаем id только что добавленного пользователя
        if phone_numbers:
            for phone in phone_numbers:
                cur.execute("INSERT INTO phones (client_id, phone) VALUES (%s, %s)", (client_id, phone))
        conn.commit()
        print("User added successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or adding new user: ", error)
    finally:
        if conn:
            cur.close()
            conn.close()

# Пример использования функции:
add_new_user("John", "Doe", "john.doe@example.com", ["555-1234", "555-5678"])
