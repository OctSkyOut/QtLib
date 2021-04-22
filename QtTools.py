# 해당 라이브러리 사용하기 위한 조건
# 1. 기본 라이브러리 사용
# 2. pyQt 사용시 타이머 재연결 기능 제공
# 3. pyQt 이외의 기본 타이머로 재연결 기능 제공

import os
from typing import TypeVar
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QStackedWidget, QMainWindow
from PyQt5.QtCore import QTimer
import threading
import time

# T타입은 QMainWindow, 메인프로그램 객체를 의미하며 윈도우에서는 사용하지 않습니다.
# 리눅스 전용입니다.
T = TypeVar("T", bound=QMainWindow)


class QtTools:
    """
    ### QtTools 클레스는 PyQt를 사용시 자주사용하는 기능들을 모아놓았습니다.
    """

    def set_interval_qt(self, time: int, callback):
        """
        ### set_interval_qt 메소드는 PyQt에서 Timer(주기적으로 함수실행)를 필요로할때
        ### 간단히 만들어주는 객체입니다.


        ### 메소드 사용시 필요한 인자\n
        time =>
            타입 : 정수형
            설명 : time에서 선언한 주기마다 callback(콜백)함수를 실행합니다.

        callback =>
            타입 : 함수형
            설명 : 주기적으로 실행시킬 함수나 메소드를 넣습니다.

        반환값 : QTimer객체
        """
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
        """
        ### set_interval_normal 메소드는 일반적인 타이머를 필요로할때
        ### 간단히 만들어주는 메소드입니다.

        ### 메소드 사용시 필요한 인자\n
        time =>
            타입 : 정수형
            설명 : time에서 선언한 주기마다 callback(콜백)함수를 실행합니다.

        callback =>
            타입 : 함수형
            설명 : 주기적으로 실행시킬 함수나 메소드를 넣습니다.

        반환값 : Thread.Timer객체
        """
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


class QtEventTools:
    """
    ### QtEventTools 클레스는 PyQt를 자주사용하는 이벤트 기능들을 모아놓았습니다.
    """

    # 설명 : 다른 위젯으로 페이지 이동할 때 사용
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # currentPage = 현재 페이지 QWidget객체
    # nextPage = 다음 페이지 QWidget객체
    def move_page(self, pagewidget: QStackedWidget, nextPage: QWidget) -> None:
        """
        ### move_page 메소드는 일반적인 다음 화면으로 넘어가기위해
        ### 간단히 만들어줄 메소드입니다.

        ### 메소드 사용시 필요한 인자\n
        pagewidget =>
            타입 : QStackedWidget
            설명 : 페이지 위젯 객체(다음 페이지의 상위객체)를 입력합니다. (Qt디자이너 객체탐색기 참고.)

        nextPage =>
            타입 : QWidget
            설명 : 다음 화면으로 넘길 객체를 입력합니다.

        반환값 : 없음
        """
        try:
            pagewidget.setCurrentWidget(nextPage)
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
    def set_text(self, widgetObj: object, text: str):
        """
        ### set_text 메소드는 텍스트를 바꿀 때 사용하는 메소드입니다.
        ### 기본적으로 Label객체 이외에는 repaint()메소드를 사용할 필요가 없지만,
        ### Label객체같은경우, repaint()를 사용해야만 Qt에서 버그가 일어나지 않는다.
        ### * setText 메소드가 없는 위젯 객체일 경우 해당 메소드가 없다는 오류를 발생시킨다.

        ### 메소드 사용시 필요한 인자\n
        widgetObj =>
            타입 : object
            설명 : PyQt에서 제공하는 모든위젯이며, 텍스트를 바꾸기 위한 객체를 입력한다.

        text =>
            타입 : 문자열
            설명 : 위젯에 설정 할 문자열을 넣는다.

        반환값 : 없음
        """
        try:
            widgetObj.setText(text)

            if isinstance(widgetObj, (QLabel,)) == True:
                widgetObj.repaint()

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

    def timespan_to_dict(self, timespan: float) -> dict:
        """
        ### timespan_to_dict 메소드는 초를 시, 분, 초로 바꿀 때 사용하는 메소드입니다.
        ### 주로 타이머나 시간과 관련된 기능을 구현할 때 사용하면 편리합니다.

        ### 메소드 사용시 필요한 인자\n
        timespan =>
            타입 : 실수형
            설명 : 시,분,초를 모두 초로 만들어 계산된 값을 넣습니다,

        반환값 : 딕셔너리 객체 ( {시, 분, 초}가 들어있는 객체 )
        """
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

    def program_off(self, mainObj: T):
        """
        ### program_off 메소드는 프로그램 종료를 구현할때 사용되는 메소드입니다.
        ### * 윈도우 운영체제에서는 사용이 불가능합니다.

        ### 메소드 사용시 필요한 인자\n
        mainObj =>
            타입 : 메인 객체
            설명 : 현재 프로그램의 뿌리가 되는 메인객체를 넣습니다.

        반환값 : 없음
        """
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
        """
        ### shut_down 메소드는 시스템 종료를 구현할때 사용되는 메소드입니다.
        ### * 윈도우 운영체제에서는 사용이 불가능합니다.

        ### 메소드 사용시 필요한 인자 : 없음

        반환값 : 없음
        """
        os.system("shutdown -h now")

    # 윈도우 사용 X 리눅스 O
    # 설명 : 시스템 재시작
    # 매계변수의 타입을 설정하시고, 타입을 모르겠으면 Qt Designer 객체 탐색기 슬롯을 확인하세요.
    # ------------------------------------------
    # 매계변수 설명
    # 없음
    def reboot(self):
        """
        ### reboot 메소드는 시스템 종료를 구현할때 사용되는 메소드입니다.
        ### * 윈도우 운영체제에서는 사용이 불가능합니다.

        ### 메소드 사용시 필요한 인자 : 없음

        반환값 : 없음
        """
        self.conn.close()
        self.ser.close()
        os.system("reboot")
