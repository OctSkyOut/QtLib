# 해당 라이브러리 사용하기 위한 조건
# 1. pymysql 설치 (설치 방법 : sudo pip3 install pymysql)

import pymysql
from pymysql.cursors import DictCursor


class DBConnect:
    # 해당 클래스 인스턴스 생성시 필요조건
    # 호스트(ip), user명, 패스워드, 사용할 데이터베이스
    def __init__(
        self,
        host: pymysql.STRING,
        user: pymysql.STRING,
        password: pymysql.STRING,
        db: pymysql.STRING,
    ) -> None:
        try:
            self.__conn = pymysql.connect(
                host=host, user=user, password=password, db=db
            )
        except Exception as err:
            print(
                """
                ----------------Connection Error-----------------
            """
            )
            print(err)
            print(
                """
                --------------------------------------------------
            """
            )

    # 커넥션 정보변수 리턴
    def get_connect(self):
        return self.__conn

    # 커넥션 정보 재수정시 필요
    def set_connect(
        self,
        host: pymysql.STRING,
        user: pymysql.STRING,
        password: pymysql.STRING,
        db: pymysql.STRING,
    ) -> None:
        try:
            self.__conn.close()
            self.__conn = pymysql.connect(
                host=host, user=user, password=password, db=db
            )
        except Exception as err:
            print(
                """
                ----------------Connection Error-----------------
            """
            )
            print(err)
            print(
                """
                --------------------------------------------------
            """
            )

    # DB SELECT 쿼리 실행문
    def select_excute_query(self, query: pymysql.STRING) -> dict:
        try:
            cursor = self.__conn.cursor(DictCursor)

            self.__conn.begin()
            cursor.execute(query=query)

            return cursor.fetchall()
        except Exception as err:
            print(
                """
                ----------------Query Error-----------------
            """
            )
            print(err)
            print(
                """
                ---------------------------------------------
            """
            )

    # DB INSERT, UPDATE, DELETE 쿼리 실행문
    def excute_query(self, query: pymysql.STRING) -> None:
        try:
            cursor = self.__conn.cursor()

            self.__conn.begin()
            cursor.execute(query=query)

            print(
                """Execute complete. Check your table
            쿼리 처리 성공 테이블을 확인하세요."""
            )
        except Exception as err:
            print(
                """
                ----------------Query Error-----------------
            """
            )
            print(err)
            print(
                """
                ---------------------------------------------
            """
            )

    # DB와의 연결을 종료합니다.
    def disconnect(self):
        self.__conn.close()
