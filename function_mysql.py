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
    """ 편의점 상품 목록 조회 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print('Total Products:', cursor.rowcount)
    for row in rows:
        print(row)
    return rows

def insert_product(conn, name, price, stock_quantity, code):
    """ 새로운 상품 추가 """
    query = "INSERT INTO products(name, price, stock_quantity, code) VALUES(%s, %s, %s, %s)"
    args = (name, price, stock_quantity, code)
    
    product_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id = cursor.lastrowid
    conn.commit()
    return product_id

def update_product(conn, product_id, name, price, stock_quantity, code):
    """ 상품 정보 수정 """
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
    """ 상품 삭제 """
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

    # 전체 상품 조회
    query_with_fetchall(conn)

    # 상품 추가
    name = input('상품명을 입력하세요 >>> ')
    price = int(input('가격을 입력하세요 >>> '))
    stock_quantity = int(input('재고 수량을 입력하세요 >>> '))
    code = int(input('상품 코드를 입력하세요 >>> '))
    insert_product(conn, name, price, stock_quantity, code)

    # 변경된 상품 목록 조회
    query_with_fetchall(conn)

    # 상품 수정 (사용자 입력)
    product_id = int(input('수정할 상품 ID를 입력하세요 >>> '))
    new_name = input('새 상품명을 입력하세요 >>> ')
    new_price = int(input('새 가격을 입력하세요 >>> '))
    new_stock_quantity = int(input('새 재고 수량을 입력하세요 >>> '))
    new_code = int(input('새 상품 코드를 입력하세요 >>> '))
    
    affected_rows = update_product(conn, product_id, new_name, new_price, new_stock_quantity, new_code)
    print(f'Number of affected rows: {affected_rows}')

    # 상품 삭제 (사용자 입력)
    product_id = int(input('삭제할 상품 ID를 입력하세요 >>> '))
    
    affected_rows = delete_product(conn, product_id)
    print(f'Number of affected rows: {affected_rows}')

    # 최종 상품 목록 조회
    query_with_fetchall(conn)
    
    conn.close()
