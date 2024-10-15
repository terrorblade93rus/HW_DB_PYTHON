import psycopg2

# Функция для создания структуры базы данных
def create_db():
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()
    
    # Создаем таблицу для клиентов
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(100)
    );
    ''')
    
    # Создаем таблицу для телефонов
    cur.execute('''
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
        phone VARCHAR(20)
    );
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Функция для добавления нового клиента
def add_client(first_name, last_name, email):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()
    
    cur.execute('''
    INSERT INTO clients (first_name, last_name, email) 
    VALUES (%s, %s, %s) RETURNING id;
    ''', (first_name, last_name, email))
    
    client_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return client_id

# Функция для добавления телефона существующему клиенту
def add_phone(client_id, phone):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()
    
    cur.execute('''
    INSERT INTO phones (client_id, phone) 
    VALUES (%s, %s);
    ''', (client_id, phone))
    
    conn.commit()
    cur.close()
    conn.close()

# Функция для изменения данных клиента
def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()

    if first_name:
        cur.execute('UPDATE clients SET first_name = %s WHERE id = %s', (first_name, client_id))
    if last_name:
        cur.execute('UPDATE clients SET last_name = %s WHERE id = %s', (last_name, client_id))
    if email:
        cur.execute('UPDATE clients SET email = %s WHERE id = %s', (email, client_id))
    
    conn.commit()
    cur.close()
    conn.close()

# Функция для удаления телефона клиента
def delete_phone(client_id, phone):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()
    
    cur.execute('DELETE FROM phones WHERE client_id = %s AND phone = %s', (client_id, phone))
    
    conn.commit()
    cur.close()
    conn.close()

# Функция для удаления клиента
def delete_client(client_id):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()
    
    cur.execute('DELETE FROM clients WHERE id = %s', (client_id,))
    
    conn.commit()
    cur.close()
    conn.close()

# Функция для поиска клиента по имени, фамилии, email или телефону
def find_client(search_term):
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()

    cur.execute('''
    SELECT clients.id, clients.first_name, clients.last_name, clients.email, phones.phone
    FROM clients
    LEFT JOIN phones ON clients.id = phones.client_id
    WHERE clients.first_name ILIKE %s 
    OR clients.last_name ILIKE %s
    OR clients.email ILIKE %s
    OR phones.phone ILIKE %s
    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return results

# Демонстрация работы программы
if __name__ == "__main__":
    create_db()

    # Добавляем клиента
    client_id1 = add_client('John', 'Doe', 'john@example.com')
    client_id2 = add_client('Jane', 'Smith', 'jane@example.com')

    # Добавляем телефоны клиентам
    add_phone(client_id1, '123-456-7890')
    add_phone(client_id1, '987-654-3210')
    add_phone(client_id2, '555-555-5555')

    # Изменяем данные клиента
    update_client(client_id1, first_name='Jonathan')

    # Удаляем телефон
    delete_phone(client_id1, '987-654-3210')

    # Ищем клиента
    clients = find_client('Jonathan')
    for client in clients:
        print(client)

    # Удаляем клиента
    delete_client(client_id2)
