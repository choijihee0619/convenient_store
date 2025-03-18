from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

# ========================= MySQL 연결 및 설정 =========================
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
    """ MySQL 데이터베이스 연결 """
    conn = None
    try:
        print('Connecting to MySQL database...')
        config = read_config()
        conn = MySQLConnection(**config)
    except Error as error:
        print(error)
    return conn

# ========================= 상품 관리 기능 =========================
def query_with_fetchall(conn):
    """ 편의점 상품 목록 조회 """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print("\n📦 편의점 상품 목록")
    print(f"총 상품 개수: {cursor.rowcount}")
    for row in rows:
        print(row)
    return rows

def is_code_exists(conn, code):
    """ 상품 코드 중복 검사 """
    query = "SELECT COUNT(*) FROM products WHERE code = %s"
    cursor = conn.cursor()
    cursor.execute(query, (code,))
    count = cursor.fetchone()[0]
    return count > 0  # True이면 중복 존재

def insert_product(conn):
    """ 새로운 상품 추가 (중복 코드 검사 포함) """
    name = input('상품명을 입력하세요 >>> ')
    price = int(input('가격을 입력하세요 >>> '))
    stock_quantity = int(input('재고 수량을 입력하세요 >>> '))
    code = int(input('상품 코드를 입력하세요 >>> '))

    if is_code_exists(conn, code):
        print(f"❌ 상품 코드 {code}는 이미 존재합니다. 다른 코드를 입력하세요.")
        return None

    query = "INSERT INTO products(name, price, stock_quantity, code) VALUES(%s, %s, %s, %s)"
    args = (name, price, stock_quantity, code)

    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id = cursor.lastrowid
    conn.commit()
    print(f"✅ 상품이 추가되었습니다! (ID: {product_id})")

def update_product(conn):
    """ 상품 정보 수정 """
    product_id = int(input('수정할 상품 ID를 입력하세요 >>> '))
    new_name = input('새 상품명을 입력하세요 >>> ')
    new_price = int(input('새 가격을 입력하세요 >>> '))
    new_stock_quantity = int(input('새 재고 수량을 입력하세요 >>> '))
    new_code = int(input('새 상품 코드를 입력하세요 >>> '))

    query = """ UPDATE products
                SET name = %s, price = %s, stock_quantity = %s, code = %s
                WHERE id = %s """
    
    data = (new_name, new_price, new_stock_quantity, new_code, product_id)
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()
    print(f"✅ 수정된 상품 개수: {affected_rows}")

def delete_product(conn):
    """ 상품 삭제 """
    product_id = int(input('삭제할 상품 ID를 입력하세요 >>> '))
    
    query = "DELETE FROM products WHERE id = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (product_id,))
        affected_rows = cursor.rowcount
    conn.commit()
    print(f"✅ 삭제된 상품 개수: {affected_rows}")

def search_product(conn):
    """ 상품 검색 """
    search_type = input("검색 기준을 선택하세요 (1: ID, 2: 이름, 3: 코드) >>> ").strip()

    if search_type == "1":
        product_id = int(input("검색할 상품 ID를 입력하세요 >>> "))
        query = "SELECT * FROM products WHERE id = %s"
        param = (product_id,)
    elif search_type == "2":
        name = input("검색할 상품명을 입력하세요 >>> ")
        query = "SELECT * FROM products WHERE name LIKE %s"
        param = (f"%{name}%",)
    elif search_type == "3":
        code = int(input("검색할 상품 코드를 입력하세요 >>> "))
        query = "SELECT * FROM products WHERE code = %s"
        param = (code,)
    else:
        print("❌ 잘못된 입력입니다.")
        return

    cursor = conn.cursor()
    cursor.execute(query, param)
    rows = cursor.fetchall()

    if rows:
        print("\n🔍 검색 결과")
        for row in rows:
            print(row)
    else:
        print("❌ 검색 결과가 없습니다.")

# ========================= 실행 코드 =========================
if __name__ == '__main__':
    print(__name__)
    conn = connect()

    while True:
        display = '''
-------------------------------------------------------------
1. 상품 추가, 2. 상품 수정, 3. 상품 삭제, 4. 상품 검색, 5. 상품 목록, 6. 프로그램 종료
-------------------------------------------------------------
메뉴를 선택하세요 >>> '''
        
        choice = input(display).strip()

        if choice == "1":
            insert_product(conn)
        elif choice == "2":
            update_product(conn)
        elif choice == "3":
            delete_product(conn)
        elif choice == "4":
            search_product(conn)
        elif choice == "5":
            query_with_fetchall(conn)
        elif choice == "6":
            print("프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 입력입니다. 다시 입력하세요.")

    conn.close()
