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

# ========================= 상품 목록 조회 (정렬 포함) =========================
def display_sorted_products(conn):
    """ 정렬된 상품 목록 조회 및 출력 """
    while True:
        print('''
--------------------- 정렬 기준 선택 ---------------------
1. 가격순 정렬
2. 재고 수량순 정렬
3. ID순 정렬 (기본값)
-------------------------------------------------------
        ''')
        sort_choice = input("정렬 기준을 선택하세요 >>> ").strip()

        if sort_choice == "1":
            order_by = "price"
        elif sort_choice == "2":
            order_by = "stock_quantity"
        else:
            order_by = "id"

        print('''
--------------------- 출력 개수 선택 ---------------------
1. 상위 10개만 출력
2. 전체 출력
-------------------------------------------------------
        ''')
        limit_choice = input("출력 개수를 선택하세요 >>> ").strip()

        if limit_choice == "1":
            limit = "LIMIT 10"
        else:
            limit = ""

        query = f"SELECT * FROM products ORDER BY {order_by} DESC {limit}"

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        print("\n📦 정렬된 상품 목록")
        for row in rows:
            print(row)

        break

# ========================= 상품 관리 기능 =========================
def insert_product(conn):
    """ 새로운 상품 추가 """
    name = input('상품명을 입력하세요 >>> ')
    price = int(input('가격을 입력하세요 >>> '))
    stock_quantity = int(input('재고 수량을 입력하세요 >>> '))
    code = int(input('상품 코드를 입력하세요 >>> '))

    query = "INSERT INTO products(name, price, stock_quantity, code) VALUES(%s, %s, %s, %s)"
    args = (name, price, stock_quantity, code)

    with conn.cursor() as cursor:
        cursor.execute(query, args)
        product_id = cursor.lastrowid
    conn.commit()
    print(f"✅ 상품이 추가되었습니다! (ID: {product_id})")

def update_product(conn):
    """ 상품 정보 수정 (코드 검색 + 특정 항목 선택) """
    product_code = int(input('수정할 상품의 코드(상품 코드)를 입력하세요 >>> '))

    # 해당 상품이 존재하는지 확인
    query = "SELECT id, name, price, stock_quantity, code FROM products WHERE code = %s"
    cursor = conn.cursor()
    cursor.execute(query, (product_code,))
    product = cursor.fetchone()

    if not product:
        print("❌ 해당 코드의 상품이 존재하지 않습니다.")
        return

    product_id, current_name, current_price, current_stock, current_code = product

    print(f"\n🔍 현재 상품 정보:")
    print(f"상품명: {current_name}, 가격: {current_price}, 재고 수량: {current_stock}, 코드: {current_code}")

    print('''
---------------------- 수정할 항목 선택 ----------------------
1. 상품명 변경
2. 재고 수량 변경
---------------------------------------------------------
    ''')
    choice = input("수정할 항목을 선택하세요 >>> ").strip()

    if choice == "1":
        new_name = input(f"새 상품명을 입력하세요 (현재: {current_name}) >>> ").strip()
        query = "UPDATE products SET name = %s WHERE id = %s"
        data = (new_name, product_id)
    elif choice == "2":
        new_stock = int(input(f"새 재고 수량을 입력하세요 (현재: {current_stock}) >>> "))
        query = "UPDATE products SET stock_quantity = %s WHERE id = %s"
        data = (new_stock, product_id)
    else:
        print("❌ 잘못된 입력입니다. 수정 취소.")
        return

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
1. 상품 추가, 2. 상품 수정, 3. 상품 삭제, 4. 상품 검색, 
5. 상품 목록 (정렬 및 개수 선택), 6. 프로그램 종료
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
            display_sorted_products(conn)
        elif choice == "6":
            print("프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 입력입니다. 다시 입력하세요.")

    conn.close()
