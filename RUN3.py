# 핵심코드
# -------------------------------------------------------------------------------------
# * 변수, 필드
# MyWindow.t_time
# 총 가공시간
#
# MyWindow.OUTPUT
# 아두이노 아웃풋 값 { "Sec" : 0 or 1, "Total_Count" : 0 or 1}
#
# MyWindow.user_count
# 사용자가 직접 총 생산량을 설정한 값
#
# MyWindow.sub_time
# 1개의 완제품을 만드는데 걸리는 시간
#
# MyWindow.total_count
# 완제품 개수
#
# MyWindow.new_count_signal
# 아두이노에서 "Total_Count" 값이 1이나 0일때 저장함
#
# MyWindow.delay
# DB에 전송 할 때 지연 플레그
#
# MyWindow.count_flag
# 카운트 값이 들어왔을 때 True 시간값일 때는 False 둘 다 안들어올 때도 False
#
# MyWindow.ser
# 아두이노 시리얼 값을 불러오기 위한 객체
#
# MyWindow.conn
# 데이터베이스 연결 객체
#
# MyWindow.timer
# SerialWorker의 QThread객체를 담고있다
# QThread객체란 : 일반 쓰레드를 사용하거나 다른 쓰레드 사용시
#                 UI 창이 닫히고 계속 실행되는 현상이 나타남
#                 이를 해결할 수 있는 방법이 Qt에서 제공하는 QTrhead를 사용하는 것이다.
#
# MainWindow.timerVar, MainWindow.timerDB
# QTimer객체를 사용하여 일정 주기마다 어떠한 메소드를 실행하게 한다.
# QTimer객체란 : setInterval과 같은 역할을 하는 객체이다.
# ------------------------------------------------------------------------------------
# * 메소드
# MainWindow.count_reset - Line 130
# 초기화 버튼을 누르면 총 가공시간, 개당 가공시간, 총 카운트가 초기화된다.
#
# rerender - Line 146
# MainWindow.timerVar를 통해서 1초마다 한번씩 실행되며 카운트 신호 또는 시간 신호에 따라
# 카운트 신호는 카운트 값을 1 늘이고, 시간신호는 시간초를 1 늘인다.
# 만약 카운트 신호가 1 들어오면 쌓였던 sub_time의 값은 초기화된다.
#
# MainWindow._db_send - Line 179
# 1분마다 1번씩 DB에 총 가공시간, 총 생산수량을 INSERT하게 한다.
#
# MainWindow.DB_connection - Line 199
# DB에 연결하는 메소드이다.
#
# MainWindow.DB_connet_save - Line 221
# DB에 총 가공시간, 총 생산수량을 INSERT하게 한다.
#
# SerialWorker.run - Line 308
# 1초마다 아두이노 시리얼을 받는다.
# 받은 값은 MyWindow.OUTPUT에 저장하고 MyWindow.sub_time과 MyWindow.t_time은
# OUTPUT["Sec"]의 값을 더하고, 완제품이 나오면 MyWindow.total_count에
# OUTPUT["Total_Count"]값을 더한다.
# ------------------------------------------------------------------------------------

from datetime import datetime
import sys
import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5.QtCore import QThread
import time
import datetime

import DBConncet as db
import GPIOArduiono as arduino
import QtTools as qt_tools

UI = uic.loadUiType("C:/Users/oct_sky_out/Desktop/HoamQt/Main.UI")[0]


class MyWindow(QMainWindow, QWidget, UI):
    def __init__(self):
        super().__init__()

        # 아두이노 출력 저장 변수
        self.OUTPUT = {}

        # 총 시간값을 담을 변수
        self.t_time = 0
        # 제품 1개를 공정하는데 걸린시간을 담는 변수
        self.sub_time = 0

        # 사용자가 입력한 완제품 수량
        self.user_count = 0
        # 제품설비가 완제품을 만든 개수
        self.total_count = 0
        # 새로운 완제품을 하나 만들때마다 들어오는 신호
        self.new_count_signal = 0
        # 시간값 초기화를 위한 변수
        self.count_flag = False
        # 데이터베이스에 데이터 저장시 원하는 저장간격
        self.delay = 0

        # btn_reset (초기화 버튼) 폰트UI 변경
        self.setupUi(self)
        font = QFont("은 굴림", 14)
        self.btn_reset.setFont(font)

        # 프로그램 첫 실행 화면설정
        self.Pages_widget.setCurrentWidget(self.Monitor_1)

        # 아두이노 시리얼 오픈
        self.ser = arduino.GpioArduino()
        self.ser.set_ardu_path("COM7")
        self.ser = self.ser.open_arduino()

        # 비동기로 시리얼데이터를 입력받고, 가공한다
        self.timer = SerialWorker(parent=self).start()

        # 1초마다 rerender함수를 실행하고 이를 프로그램 실행부터 적용한다.
        self.timerVar = qt_tools.QtTools().set_interval_qt(1000, self.rerender)
        self.timerVar.start()

        # 1초마다 db_send함수를 실행하고 이를 프로그램 실행부터 적용한다.
        self.timerDB = qt_tools.QtTools().set_interval_qt(1000, self._db_send)
        self.timerDB.start()

        # QtEventTools 객체를 생성한다.
        self.tool = qt_tools.QtEventTools()

    # 다이얼(사용자 입력카운트)의 값이 바뀌면 실행되는 이벤트이다.
    def dial_value_changed(self):
        # 사용자가 입력한 다이얼의 값을 숫자(텍스트)로 표출한다.
        self.tool.set_text(self.dial_count_number, str(self.dial_count.value()))

    # 다이얼의 값을 설정하고, 설정버튼을 누르면 호출되는 이벤트이다.
    def dial_value_set(self):
        # user_count 필드(사용자 입력 완제품수량 필드)에
        # 제조설비가 만든 완제품 수량 + 사용자가 입력한 완제품값을 더한다
        self.user_count = int(self.count.text()) + self.dial_count.value()
        # 총 가공수량에 user_count필드의 값을 표출한다.
        self.tool.set_text(self.count, str(self.user_count))

    # 초기화버튼을 누르면 실행되는 함수이다.
    def count_reset(self):
        # 다이얼의 값을 0으로 초기화시키고, 이를 렌더링하는 라벨 객체의 값도 초기화시킨다.
        self.dial_count.setValue(0)
        self.tool.set_text(self.dial_count_number, str(self.dial_count.value()))

        # 총가공수량의 렌더링 값을 0으로 바꾼다.
        self.tool.set_text(self.count, "0")
        # 사용자 입력 완제품수량 필드, 제조설비의 완제품수량을 초기화시킨다.
        self.user_count = 0
        self.total_count = 0

        # 총 설비동작 시간,
        self.t_time = 0
        self.sub_time = 0

        # 총 시간, 분, 초 그리고 제품 1개당 소요 시간, 분, 초 를 모두 00으로
        # 렌더링 초기화를 시킨다.
        self.tool.set_text(self.hour, "00")
        self.tool.set_text(self.min, "00")
        self.tool.set_text(self.sec, "00")
        self.tool.set_text(self.t_hour, "00")
        self.tool.set_text(self.t_min, "00")
        self.tool.set_text(self.t_sec, "00")

    # 1초마다 다시 렌더링, 시간, 카운터를 구별하는 메소드
    def rerender(self):
        # 제품생산 완료시 self.new_count_signal에 1이 들어간다.
        if self.new_count_signal == 1:
            self.count_flag = True
            self.total_count += self.new_count_signal
            self.tool.set_text(self.count, str(self.total_count + self.user_count))
        else:
            # 제품이 생산 중일때는 해당 블록을 실행한다.
            #          self.sub_time += self.OUTPUT["Sec"]
            if self.count_flag:
                self.sub_time = 0
                self.tool.set_text(self.hour, "00")
                self.tool.set_text(self.min, "00")
                self.tool.set_text(self.sec, "00")
                self.count_flag = False

            sub_sec = self.tool.timespan_to_dict(self.sub_time)
            self.tool.set_text(self.hour, sub_sec["hour"])
            self.tool.set_text(self.min, sub_sec["min"])
            self.tool.set_text(self.sec, sub_sec["sec"])

        #        self.t_time += self.OUTPUT["Sec"]
        total_sec = self.tool.timespan_to_dict(self.t_time)
        self.tool.set_text(self.t_hour, total_sec["hour"])
        self.tool.set_text(self.t_min, total_sec["min"])
        self.tool.set_text(self.t_sec, total_sec["sec"])

    # 데이터베이스에 1분마다 한번씩 현재까지 수집한 데이터를 보냄
    def _db_send(self):
        self.delay += 1

        if 60 == self.delay:
            self.DB_connet_save()
            self.delay = 0

    # 1분마다 데이터베이스와의 연결, 종료하며, 현재까지의 수집 데이터를
    # 데이터베이스로 보낸다.
    def DB_connet_save(self):

        self.dbconn = db.DBConnect(
            "hidatajinju.iptime.org", "hidata", "jinju7639998", "himes_hoam"
        )

        try:
            sql = f"""INSERT INTO EqTagRollUpDataHs (
                    Tagid,
                    EventDt,
                    PassDt,
                    TagValue
                ) VALUES (
                "0002",
                '{str(datetime.datetime.now())}',
                '{self.hour.text()}{self.min.text()}{self.sec.text()}',
                '{self.count.text()}'
                )"""

            # SQL문 처리 및 처리 후 데이터베이스 연결 종료
            self.dbconn.excute_query(query=sql, close=True)
        except Exception as err:
            print(
                """
                ----------------SAVE ERROR--------------------
                """
            )
            print(err)
            print(
                """
                ----------------------------------------------
                """
            )


# 아두이노 시리얼을 비동기로 실행하기 위해 만든 클래스이다.
class SerialWorker(QThread):
    # 객체가 처음 생성 될 시 부모를 설정해준다.
    def __init__(self, parent: MyWindow = None):
        super().__init__(parent)

    # 스레드가 비동기로 실행할때 사용되는 코드이다.
    def run(self):
        while True:
            try:
                # 아두이노에서 나오는 출력은 1 또는 0이다.
                # OUTPUT에 아두이노 값(JSON)을 1초마다 읽고 파이썬 딕셔너리로 만들어준다.
                self.parent().OUTPUT = json.loads(self.parent().ser.readline().decode())
                # print(self.parent().OUTPUT)
                # 1초마다 총 생산시간, 개당 생산시간에 OUTPUT["Sec"] 값을 더한다.
                self.parent().t_time += self.parent().OUTPUT["Sec"]
                self.parent().sub_time += self.parent().OUTPUT["Sec"]

                # 생산완료 카운트 신호가 들어 올 시 new_count_signal에 카운트 신호를 넣는다.
                self.parent().new_count_signal = self.parent().OUTPUT["Total_Count"]
                # pyqt에서 반복적인 일을 하는 메소드에는 해당 구문을 집어넣어주어야 한다.
                QApplication.processEvents()

                print(self.parent().OUTPUT["Total_Count"])
                print(self.parent().OUTPUT["Sec"])
                QThread.sleep(0.5)
            except:
                continue


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
