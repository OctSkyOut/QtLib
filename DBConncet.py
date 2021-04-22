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
        """
        ### DBConnect 객체는 데이터베이스와의 연결이 필요할 때 사용하는 객체입니다.

        ### 객체 생성시 필요한 인자\n
        host :
            타입 : 문자열
            설명 : 연결할 데이터베이스의 host 주소를 입력합니다 (IP주소를 입력합니다.)
        user :
            타입 : 문자열
            설명 : 데이터베이스 연결시 사용자계정을 입력합니다.
        password :
            타입 : 문자열
            설명 : 데이터베이스 연결시 계정의 비밀번호를 적습니다.
        db :
            타입 : 문자열
            설명 : 사용할 데이터베이스를 입력합니다.

        반환값 : 없음
        """
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
        """
        ### get_connect 메소드는 데이터베이스와 연결한 객체를 리턴합니다.

        메소드 사용시 필요한 인자 : 없음
        반환값 : 없음
        """
        return self.__conn

    # 커넥션 정보 재수정시 필요
    def set_connect(
        self,
        host: pymysql.STRING,
        user: pymysql.STRING,
        password: pymysql.STRING,
        db: pymysql.STRING,
    ) -> None:
        """
        ### set_connect 메소드는 데이터베이스와의 재연결 또는 연결정보 수정이 필요할 때 사용하는 메소드입니다.

        ### 메소드 사용시 필요한 인자\n
        host :
            타입 : 문자열
            설명 : 재연결할 데이터베이스의 host 주소를 입력합니다 (IP주소를 입력합니다.)
        user :
            타입 : 문자열
            설명 : 데이터베이스 재연결시 사용자계정을 입력합니다.
        password :
            타입 : 문자열
            설명 : 데이터베이스 재연결시 계정의 비밀번호를 적습니다.
        db :
            타입 : 문자열
            설명 : 사용할 데이터베이스를 입력합니다.

        반환값 : 없음
        """
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
    def select_excute_query(self, query: pymysql.STRING, close=False) -> dict:
        """
        ### select_excute_query 메소드는 SQL쿼리에서 SELECT문을 수행합니다.\n
        ### 116번째줄의  self.__conn.cursor(DictCursor)는 커서가 SELECT문을 수행하고
        ### 수행값을 딕셔너리 객체로 반환받기 위해 DictCursor 클래스를 사용하였습니다.

        ### * 오류발생시 롤백 기능이있어 수행하기 이전의 상태로 돌아갑니다.\n

        ### 메소드 사용시 필요한 인자\n
        query :
            타입 : 문자열
            설명 : 사용자가 입력하는 SELECT문 쿼리입니다.

        close:
            타입 : 불리언
            설명 : 사용자가 쿼리 수행 후 해당 데이터베이스와의 연결을 끊기를 원한다면 True를 입력
                    연결유지를 원한다면 기본값 False를 사용합니다.

        반환값 : 딕셔너리 객체
        """
        try:
            cursor = self.__conn.cursor(DictCursor)

            self.__conn.begin()
            cursor.execute(query=query)
            self.__conn.commit()

            if close == True:
                self.__conn.close()

            return cursor.fetchall()
        except Exception as err:
            self.__conn.rollback()
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
    def excute_query(self, query: pymysql.STRING, close=False) -> None:
        """
        ### excute_query 메소드는 SQL쿼리에서 INSERT, UPDATE, DELETE문을 수행합니다.\n
        ### 반환값은 없지만 성공적으로 수행시 성공메세지를 콘솔에 알립니다.

        ### 오류발생시 롤백 기능이있어 수행하기 이전의 상태로 돌아갑니다.\n

        메소드 사용시 필요한 인자\n
        query :
            타입 : 문자열
            설명 : 사용자가 입력하는 INSERT, UPDATE, DELETE문 쿼리입니다.

        close:
            타입 : 불리언
            설명 : 사용자가 쿼리 수행 후 해당 데이터베이스와의 연결을 끊기를 원한다면 True를 입력
                    연결유지를 원한다면 기본값 False를 사용합니다.

        반환값 : 없음
        """
        try:
            cursor = self.__conn.cursor()

            self.__conn.begin()
            cursor.execute(query=query)
            self.__conn.commit()

            print(
                """Execute complete. Check your table
            쿼리 처리 성공 테이블을 확인하세요."""
            )

            if close == True:
                self.__conn.close()
        except Exception as err:
            self.__conn.rollback()
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
        """
        ### disconnect 메소드는 해당 데이터베이스와의 연결을 해재하고싶은 경우 사용합니다.

        메소드 사용시 필요한 인자 : 없음
        반환값 : 없음
        """
        self.__conn.close()
