from configparser import Error
import os
from sys import path
from serial import Serial


class GpioArduino:
    def __init__(self) -> None:
        """
        ### GpioArduino 클래스를 생성시 기본적인 GPIO루트, 아두이노 연결루트를 설정합니다

        ### 객체 생성시 필요한 인자 : 없음
        """
        self.__gpio_path = "/sys/bus/w1/devices/"
        self.__ardu_path = "/dev/ttyACM0"

    def set_gpio_path(self, path: str):
        """
        ### set_gpio_path 메소드 사용시 GPIO루트를 바꿀 수 있습니다.

        ### 메소드 사용시 필요한 인자 :
            path =>
                타입 : 문자열
                설명 : GPIO의 위치 정보가 바뀌었을 시 사용합니다.

            반환값 : 없음
        """
        self.__gpio_path = path

    def set_ardu_path(self, path: str):
        """
        ### set_ardu_path 메소드 사용시 아두이노 루트를 바꿀 수 있습니다.

        ### 메소드 사용시 필요한 인자
            path =>
                타입 : 문자열
                설명 : 아두이노의 정보가 바뀌었을 시 사용합니다.

            반환값 : 없음
        """
        self.__ardu_path = path

    def get_gpio(self):
        """
        ### get_gpio 메소드 GPIO의 객체를 받을 수 있습니다

        ### 메소드 사용시 필요한 인자 : 없음

        ### 반환값 : 없음
        """
        return self.__gpio_path

    def get_ardu(self):
        """
        ### get_ardu 메소드 아두이노 수신 객체를 받을 수 있습니다

        ### 메소드 사용시 필요한 인자 : 없음

        ### 반환값 : 없음
        """
        return self.__ardu_path

    def read_raw_GPIO(self, gpioId: str):
        """
        ### read_raw_GPIO 메소드 GPIO의 수신데이터를 측정 후 데이터 가공없이 순수한 값을 반환합니다..

        ### 메소드 사용시 필요한 인자 :
            gpioId =>
                타입 : 문자열
                설명 : GPIO의 ID값

        ### 반환값 : 리스트 객체
        """
        try:
            os.system("modprobe w1-gpio")
            os.system("modprobe w1-therm")
            gpio = self.__gpio_path + gpioId + "/w1_slave"
            f = open(gpio, "r")
            lines = f.readlines()
            f.close()
            return lines

        except Exception as err:
            print(
                """
                    ----------------GPIO Access Error-----------------
                """
            )
            print(err)
            print(
                """
                ------------------------------------------------------
            """
            )

    def get_GPIO_id(self) -> str:
        """
        ### get_GPIO_id 메소드는 GPIO의 고유 ID값을 확인 후 ID값을 반환합니다..

        ### 메소드 사용시 필요한 인자 : 없음
        ### 반환값 : 문자열
        """
        try:

            file_list = os.listdir(self.__gpio_path)

            if len(file_list) == 1:
                return "GPIO가 존재하지 않습니다."
            elif len(file_list) >= 2:
                for i in range(0, len(file_list)):
                    if file_list[i] != "w1_bus_master1":
                        return str(file_list[i])

        except Exception as err:
            print(
                """
                    ----------------GPIO Access Error-----------------
                """
            )
            print(err)
            print(
                """
                ------------------------------------------------------
            """
            )

    # 설명 : GPIO의 연결여부 확인 및 GPIO ID값을 가져옴
    # ------------------------------------------
    # 매계변수 설명
    # boradrate : 보드레이트 설정, 기본값 => 9600
    # -------------------------------------------
    # 반환값 : 시리얼 객체
    def open_arduino(self, bordrate: int = 9600) -> Serial:
        """
        ### open_arduino 메소드는 아두이노의 시리얼 포트를 열어 값을 측정 후
        ### 시리얼 객체를 재반환합니다.

        ### 메소드 사용시 필요한 인자 :
         bordrate (선택) =>
            타입 : 정수
            설명 : 보드레이트의 기본값은 9600이다. 사용자가 직접 설정도 가능하다.

        ### 반환값 : 시리얼 객체
        """
        try:
            ser = Serial(self.__ardu_path, bordrate, timeout=1)
            if not ser.isOpen():
                ser.open()

            return ser
        except Exception as err:
            print(
                """
                    ----------------Arduino Access Error-----------------
                """
            )
            print(err)
            print(
                """
                ---------------------------------------------------------
            """
            )
