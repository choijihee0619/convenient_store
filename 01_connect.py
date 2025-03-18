from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

def read_config(filename='app.ini', section='mysql'):    
    config = ConfigParser()
    config.read(filename)
    data = {}
    if config.has_section(section):
        items = config.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception(f'{section} section not found in the {filename} file')
    return data

def connect():
    conn = None
    try:
        print('Connecting to MySQL database...')
        config = read_config()
        conn = MySQLConnection(**config)
    except Error as error:
        print(error)
    return conn

def query_with_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from products")
    rows = cursor.fetchall()
    print('Total Row(s):', cursor.rowcount)
    for row in rows:
        print(row)
    return rows

def insert_product(conn, name, code):
    query = "INSERT INTO products(name,code) " \
            "VALUES(%s,%s)"

    args = (name, code)
    product_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id =  cursor.lastrowid
    conn.commit()
    return product_id

def update_book(conn, book_id, title):
    query = """ UPDATE books
                SET title = %s
                WHERE id = %s """
    
    data = (title, book_id)
    affected_rows = 0
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()
    return affected_rows

def delete_book(conn, book_id):
    query = "DELETE FROM books WHERE id = %s"
    data = (book_id, )
    affected_rows = 0
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()
    return affected_rows


if __name__ == '__main__':
    print(__name__)
    print(read_config())
    conn = connect()

    query_with_fetchall(conn)
    product_name = input('상품명을 입력하세요 >>> ')
    code = input('code번호 입력(11자리) >>> ')
    insert_product(conn, product_name, code)
    query_with_fetchall(conn)

    # affected_rows = update_book(conn, 37, 'The Giant Book of Poetry')
    # print(f'Number of affected rows: {affected_rows}')

    # affected_rows = delete_book(conn, 37, 'The Giant Book of Poetry')
    # print(f'Number of affected rows: {affected_rows}')
    # query_with_fetchall(conn)
    conn.close()

    