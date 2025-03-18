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

def insert_product(conn, name, price, stock_quantity, code):
    query = "INSERT INTO products(name, price, stock_quantity, code) " \
            "VALUES(%s,%s,%s,%s)"

    args = (name, price, stock_quantity, code)
    product_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id =  cursor.lastrowid
    conn.commit()
    return product_id

def update_product(conn, product_id, name, price, stock_quantity, code):
    query = """ UPDATE products
                SET name = %s, price = %s, stock_quantity = %s, code = %s
                WHERE id = %s """
    
    data = (name, price, stock_quantity, code, product_id)
    affected_rows = 0
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()
    return affected_rows

def delete_product(conn, product_id):
    query = "DELETE FROM products WHERE id = %s"
    data = (product_id, )
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
    name = input('상품명을 입력하세요 >>> ')
    price = input('가격을 입력하세요 >>> ')
    stock_quantity = input('수량을 입력하세요 >>> ')
    code = input('code번호 입력(4자리) >>> ')
    insert_product(conn, name, price, stock_quantity, code)
    query_with_fetchall(conn)

    product_id = int(input("수정할 상품 ID 입력 >>> "))
    name = input("새 상품명 입력 >>> ")
    price = float(input("새 가격 입력 >>> "))
    stock_quantity = int(input("새 수량 입력 >>> "))
    code = input("새 code 번호 입력(4자리) >>> ")

    affected_rows = update_product(conn, product_id, name, price, stock_quantity, code)
    print(f'수정된 행 수: {affected_rows}')

    product_id = int(input("삭제할 상품 ID 입력 >>> "))
    affected_rows = delete_product(conn, product_id)
    print(f'삭제된 행 수: {affected_rows}')
    query_with_fetchall(conn)
    conn.close()

    