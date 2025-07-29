# 편의점 상품 관리 시스템 🏪

MySQL과 Python을 활용한 콘솔 기반 편의점 상품 관리 프로그램입니다.

## 📋 프로젝트 개요

편의점에서 상품을 효율적으로 관리할 수 있도록 개발한 CRUD 기반 관리 시스템입니다. 
데이터베이스 설계부터 사용자 인터페이스까지 전체적인 개발 과정을 경험할 수 있었던 프로젝트입니다.

## 🛠 기술 스택

- **언어**: Python 3.x
- **데이터베이스**: MySQL
- **라이브러리**: 
  - `mysql-connector-python` - MySQL 연결
  - `configparser` - 설정 파일 관리

## ✨ 주요 기능

### 1. 상품 관리
- **상품 추가**: 상품명, 가격, 재고 수량, 상품 코드 입력
- **상품 수정**: 상품 코드로 검색 후 상품명 또는 재고 수량 변경
- **상품 삭제**: 상품 ID로 특정 상품 삭제

### 2. 상품 조회 및 검색
- **다중 검색**: ID, 상품명, 상품 코드로 검색 (부분 문자열 검색 지원)
- **정렬 기능**: 가격순, 재고 수량순, ID순 정렬
- **출력 제한**: 상위 10개 또는 전체 출력 선택

### 3. 데이터베이스 연동
- 설정 파일(`app.ini`)을 통한 DB 연결 관리
- 파라미터화된 쿼리로 SQL 인젝션 방지
- 트랜잭션 관리를 통한 데이터 일관성 보장

## 🗂 프로젝트 구조

```
convenient_store/
├── convenient_store_func.py  # 메인 실행 파일
├── function_mysql.py         # 개선된 버전 (이모지 UI 포함)
├── connect_test.py          # DB 연결 및 기본 CRUD 테스트
├── app.ini                  # MySQL 연결 설정
└── README.md
```

## 🚀 실행 방법

### 1. 환경 설정
```bash
pip install mysql-connector-python
```

### 2. 데이터베이스 설정
```sql
CREATE DATABASE convenient_store;
USE convenient_store;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    stock_quantity INT NOT NULL,
    code INT UNIQUE NOT NULL
);
```

### 3. 설정 파일 수정
`app.ini` 파일에서 MySQL 연결 정보를 환경에 맞게 수정

### 4. 프로그램 실행
```bash
python convenient_store_func.py
```

## 💡 개발 고려사항

- **보안**: 파라미터화된 쿼리 사용으로 SQL 인젝션 방지
- **예외 처리**: DB 연결 실패 및 잘못된 입력에 대한 적절한 처리
- **사용자 경험**: 직관적인 메뉴 구성과 명확한 안내 메시지
- **코드 구조**: 기능별 함수 분리로 유지보수성 향상

## 📈 향후 개선 계획

- 웹 인터페이스 추가 (Flask/Django)
- 상품 카테고리 관리 기능
- 판매 기록 및 통계 기능
- 재고 부족 알림 시스템