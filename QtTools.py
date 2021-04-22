# 해당 라이브러리 사용하기 위한 조건
# 1. 기본 라이브러리 사용
# 2. pyQt 사용시 타이머 재연결 기능 제공
# 3. pyQt 이외의 기본 타이머로 재연결 기능 제공

import os
from typing import TypeVar
from PyQt5.QtWidgets import QLabel, QWidget, QStackedWidget, QMainWindow
from PyQt5.QtCore import QTimer
import threading
import time

T = TypeVar("T", bound=QMainWindow)


class QtTools:
    # 매계변수설명
    # time = 시간 ms
    # callback = 콜백함수 (꼭 함수이름를 넣어야함 괄호 사용 불가)
    def set_interval_qt(self, time: int, callback):
        try:
            qt_timer = QTimer()
            qt_timer.setInterval(time)
            qt_timer.timeout.connect(callback)
            return qt_timer
        except Exception as err:
            print(
                """
                ----------------Interval Error-----------------
            """
            )
            print(err)
            print(
                """
                -----------------------------------------------
            """
            )

    # 매계변수설명
    # time = 시간 ms
    # callback = 콜백함수 (꼭 함수이름를 넣어야함 괄호 사용 불가)
    def set_interval_normal(self, time: int, callback):
        try:
            normal_timer = threading.Timer(interval=time, function=callback)
            return normal_timer
        except Exception as err:
            print(
                """
                ----------------Interval Error-----------------
            """
            )
            print(err)
            print(
                """
                -----------------------------------------------
            """
            )

    # 설명 : 다른 위젯으로 페이지 이동할 때 사용
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # currentPage = 현재 페이지 QWidget객체
    # nextPage = 다음 페이지 QWidget객체
    def move_page(self, widget: QStackedWidget, nextPage: QWidget) -> None:
        try:
            widget.setCurrentWidget(nextPage)
        except Exception as err:
            print(
                """
                ----------------MovePage Error-----------------
            """
            )
            print(err)
            print(
                """
                -----------------------------------------------
            """
            )

    # 설명 : 라벨 텍스트를 바꿀 때는 reapint()를 넣어주어야함
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # labelObj = 라벨 객체
    # text = 라벨 객체에 새로 바꿀 텍스트
    def label_set_text(self, labelObj: QLabel, text: str):
        try:
            labelObj.setText(text)
            labelObj.repaint()
        except Exception as err:
            print(
                """
                ----------------SetText Error-----------------
            """
            )
            print(err)
            print(
                """
                -----------------------------------------------
            """
            )

    # 설명 : 타이머 기능을 구현 할 때 필요한 기능
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # timespan = 시, 분, 초를 초로만든 값 ex. 1시간 1분 30초 => 3690
    # 3690값이 timespan 매계변수에 들어가야함
    # -------------------------------------------
    # 반환값 : 딕셔너리 객체
    # { hour : int, min : int, sec : int }
    # 사용 예) time_to_string(1000)['min']
    def timespan_to_dict(self, timespan: float) -> dict:
        try:
            return {
                "hour": time.strftime("%H", time.gmtime(timespan)),
                "min": time.strftime("%M", time.gmtime(timespan)),
                "sec": time.strftime("%S", time.gmtime(timespan)),
            }
        except Exception as err:
            print(
                """
                ----------------Time Chnage Error-----------------
            """
            )
            print(err)
            print(
                """
                ---------------------------------------------------
            """
            )

    # 윈도우 사용 X 리눅스 O
    # 설명 : 프로그램 종료 기능
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # mainObj = 메인 윈도우 객체 사용시 self사용 가능
    def program_off(self, mainObj: T):
        mainObj.close()
        pid = os.getpid()
        os.system("kill -9 " + str(pid))

    # 윈도우 사용 X 리눅스 O
    # 설명 : 전원종료
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # 없음
    def shut_down(self):
        os.system("shutdown -h now")

    # 윈도우 사용 X 리눅스 O
    # 설명 : 시스템 재시작
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # 없음
    def reboot(self):
        self.conn.close()
        self.ser.close()
        os.system("reboot")