def book_input(books):
    while True:
        book_number = input(" 번호를 입력하세요(4자리로 설정하시오) >>> ")
        check = 0 # 중복확인
        for book in books :
            if book["ISBN"] == book_number: #번호가 존재하면
                check = 1 # 중복 확인 변수 변경
                print("중복된 번호입니다. 새로운 번호로 다시 입력하세요.")
                break # 중복 발견 시 루프 종료
            
        if check == 0:
            break
        
    book_title = input(" 제목을 입력하세요 >>> ")
    book_author = input(" 저자를 입력하세요 >>> ")

    books.append({"ISBN" : book_number, "제목" : book_title, "저자" : book_author, "대여 여부" : False})
    print("도서가 추가되었습니다.")
    return books

def book_update(books):
        while True:
            # 도서 리스트 출력 (수정할 때마다 최신 리스트를 보여줌)
            print("\n현재 보유 중인 도서 리스트:")
            for i in range(len(books)):
                print(f"{i + 1}. {books[i]['제목']} (ISBN: {books[i]['ISBN']}, 저자: {books[i]['저자']}, 대여 여부: {books[i]['대여 여부']})")
            
            # 수정할 도서 번호 입력
            book_num = input('수정할 도서 번호 입력 > ').strip()

            if 1 <= int(book_num) <= len(books):
                book_num = int(book_num) - 1  # 인덱스는 0부터 시작하므로
                break
            else:
                print("해당 번호가 없습니다. 다시 입력해주세요.")

        while True:
            print("\n수정할 항목을 선택하세요:")
            print("1. ISBN")
            print("2. 제목")
            print("3. 저자")
            
            number = int(input('수정할 부분 > ').strip())

            if 1 <= number <= 3:
                break
            else:
                print("잘못된 번호입니다. 1~3 사이의 번호를 입력해주세요.")

        # 도서 수정 부분
        if number == 1:
            while True:
                new_isbn = input(f'새 ISBN을 입력하세요 (기존 ISBN: {books[book_num]["ISBN"]}): ').strip()
                
                # ISBN 중복 체크
                isbn_exists = False
                for book in books:
                    if book["ISBN"] == new_isbn:
                        isbn_exists = True
                        break
                
                if new_isbn == books[book_num]["ISBN"]:
                    print("ISBN이 기존과 동일합니다. 다시 입력하세요.")
                elif isbn_exists:
                    print("이미 존재하는 ISBN입니다. 다른 ISBN을 입력해주세요.")
                else:
                    books[book_num]["ISBN"] = new_isbn
                    print(f"ISBN이 수정되었습니다: {books[book_num]['ISBN']}")
                    break

        elif number == 2:
            new_title = input(f'새 제목을 입력하세요 (기존 제목: {books[book_num]["제목"]}): ').strip()
            books[book_num]["제목"] = new_title
            print(f"제목이 수정되었습니다: {books[book_num]['제목']}")

        elif number == 3:
            new_author = input(f'새 저자를 입력하세요 (기존 저자: {books[book_num]["저자"]}): ').strip()
            books[book_num]["저자"] = new_author
            print(f"저자가 수정되었습니다: {books[book_num]['저자']}")


        # 수정 후 최신 도서 정보 출력
        print(f"수정된 도서 정보: {books[book_num]}")
        return books

def book_delete(books):
    if not books:
        print("경고: 삭제할 도서가 없습니다.")
        return
    
    remove_isbn = input("삭제할 도서의 ISBN을 입력하세요. >>> ").strip()
    
    def find_book_index(isbn):
        #ISBN을 기준으로 도서의 인덱스를 찾는 함수
        for index, book in enumerate(books):
            if book["ISBN"] == isbn:
                return index
        return None
    
    index = find_book_index(remove_isbn)
    
    if index is not None:
        print(f"'{books[index]['제목']}' 도서를 삭제하시겠습니까? 예 / 아니요 >>> ")
        answer = input("예 / 아니요: ").strip()
        
        if answer == '예':
            del books[index]
            print(f"'{remove_isbn}' 도서가 삭제되었습니다.")
        else:
            print("삭제를 취소합니다.")
    else:
        print("해당 ISBN의 도서를 찾을 수 없습니다.")

def book_search(books):

    search_type = input("검색할 기준을 선택하세요 (1: ISBN, 2: 제목, 3: 저자, Enter: 전체 목록) >>> ").strip()
    search_value = ""
    
    def filter_books(criteria, value):
        # 주어진 기준과 값에 따라 도서를 필터링하는 함수
        if criteria == "ISBN":
            return [book for book in books if book["ISBN"] == value]
        elif criteria == "제목":
            return [book for book in books if value.lower() in book["제목"].lower()]
        elif criteria == "저자":
            return [book for book in books if value.lower() in book["저자"].lower()]
        return books  # 전체 목록 반환
    
    if search_type == "1":
        search_value = input("검색할 ISBN을 입력하세요 >>> ").strip()
        found_books = filter_books("ISBN", search_value)
    elif search_type == "2":
        search_value = input("검색할 제목을 입력하세요 >>> ").strip()
        found_books = filter_books("제목", search_value)
    elif search_type == "3":
        search_value = input("검색할 저자를 입력하세요 >>> ").strip()
        found_books = filter_books("저자", search_value)
    else:
        found_books = books  # 전체 목록 출력
    
    if not found_books:
        print("❌ 검색된 도서가 없습니다.")
    else:
        print("\n📖 도서 목록")
        for i, book in enumerate(found_books, start=1):
            print(f"{i}. ISBN: {book['ISBN']} | 제목: {book['제목']} | 저자: {book['저자']} | 대여 여부: {'대여 중' if book['대여 여부'] else '대여 가능'}")

def book_rent(books):
        search = input("검색할 도서의 ISBN 또는 제목을 입력하세요 >>> ").strip()
        found_books = [book for book in books if book["ISBN"] == search or book["제목"] == search]
  
        if not found_books:
            print("❌ 해당 도서를 찾을 수 없습니다.")
        else:
            for i, book in enumerate(found_books, start=1):
                print(f"{i}. ISBN: {book['ISBN']} | 제목: {book['제목']} | 저자: {book['저자']} | 대여 여부: {'대여 중' if book['대여 여부'] else '대여 가능'}")

                select = input("대여/반납할 도서의 번호를 선택하세요 (취소: 0) >>> ").strip()

            if select.isdigit():
                select = int(select)
                if select == 0:
                    print("❌ 도서 대여/반납을 취소했습니다.")
                elif 1 <= select <= len(found_books):
                    selected_book = found_books[select - 1]

                    if selected_book["대여 여부"]:  # 이미 대여 중인 경우
                        confirm = input(f"🔄 '{selected_book['제목']}'을(를) 반납하시겠습니까? (예/아니요) >>> ").strip()
                        if confirm.lower() == "예":
                            selected_book["대여 여부"] = False
                            print(f"✅ '{selected_book['제목']}'이(가) 반납되었습니다.")
                        else:
                            print("❌ 반납이 취소되었습니다.")
                    else:  # 대여 가능한 경우
                        confirm = input(f"📖 '{selected_book['제목']}'을(를) 대여하시겠습니까? (예/아니요) >>> ").strip()
                        if confirm.lower() == "예":
                            selected_book["대여 여부"] = True
                            print(f"✅ '{selected_book['제목']}'이(가) 대여되었습니다.")
                        else:
                            print("❌ 대여가 취소되었습니다.")
                else:
                    print("❌ 잘못된 번호입니다.")
            else:
                print("❌ 숫자로 입력해주세요.")
          
