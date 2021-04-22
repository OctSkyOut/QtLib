from configparser import Error
import os
from sys import path
from serial import Serial


class GpioArduino:
    def __init__(self) -> None:
        self.__gpio_path = "/sys/bus/w1/devices/"
        self.__ardu_path = "/dev/ttyACM0"

    def set_gpio_path(self, path: str):
        self.__gpio_path = path

    def set_ardu_path(self, path: str):
        self.__ardu_path = path

    def set_gpio_path(self, path: str):
        self.__gpio_path = path

    def set_ardu_path(self, path: str):
        self.__ardu_path = path

    # 설명 : GPIO의 데이터를 가져옴 (가공되지않은 데이터)
    # ------------------------------------------
    # 매계변수 설명
    # gpioId : GPIO의 고유값을 가져와야합니다.
    # -------------------------------------------
    # 반환값 : 리스트 객체
    def read_raw_GPIO(self, gpioId: str):
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

    # 설명 : GPIO의 연결여부 확인 및 GPIO ID값을 가져옴
    # ------------------------------------------
    # 매계변수 설명
    # 없음
    # -------------------------------------------
    # 반환값 : 문자열
    # GPIO ID 값
    def get_GPIO_id(self) -> str:
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
