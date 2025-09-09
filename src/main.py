#!/usr/bin/env python3
# pylint: disable=import-error

"""
GPIO 과제
- gpiozero 라이브러리 사용

UART 과제
- pyserial 라이브러리 사용
- UART 통신: 115200 bps, 8N1, 플로우 제어 없음
- TXD3/RXD3을 활용
"""

import sys
import time

from gpiozero import LED, Button
from serial import Serial


def blink_led() -> None:
    """
    [문제 1] 18번 핀에 연결된 LED를 1초 간격으로 ON/OFF를 10번 반복
    - gpiozero.LED 사용
    - 종료시 LED는 OFF 상태
    """
    # TODO: blink_led 구현
    led = LED(18)
    for _ in range(10):
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)


def check_to_input_button() -> None:
    """
    [문제 2] 18번 핀 버튼 입력을 받아서
      - 눌렸을 때: 'pressed'
      - 뗐을 때:   'released'
    를 출력한다.
    - polling 방식으로 구현할 것.
    - 버튼 입력을 10번 받았으면 종료.
    """
    # TODO: check_to_input_button 구현
    button = Button(18)
    press_count = 0  # 버튼이 눌린 횟수를 세는 카운터
    was_pressed = False

    while press_count < 10:
        # 현재 버튼 상태
        is_pressed_now = button.is_pressed

        # 이전에는 눌리지 않았는데 지금 눌렸다면 (상태가 Low -> High로 변경)
        if is_pressed_now and not was_pressed:
            print('pressed')
            press_count += 1

        # 이전에는 눌려있었는데 지금 떼졌다면 (상태가 High -> Low로 변경)
        elif not is_pressed_now and was_pressed:
            print('released')

        # 다음 루프를 위해 현재 상태를 저장
        was_pressed = is_pressed_now
        time.sleep(0.01)  # CPU 과부하 방지


def blink_led_through_button() -> None:
    """
    [문제 3]
    - 12번: LED 출력
    - 13번: Button 입력
    - 버튼이 눌려 있는 동안에만 LED가 0.5초 간격으로 깜빡인다.
    - 버튼이 10번 눌려졌으면 종료.
    - 종료시 LED는 OFF 상태
    """
    # TODO: blink_led_through_button 구현
    led = LED(12)
    btn = Button(13, pull_up=True)
    num = 0
    while num < 10:
        if btn.is_pressed:
            led.on()
            time.sleep(0.5)
            led.off()
        if btn.is_pressed:
            num += 1
            break
    led.off()


def transmit_msg() -> None:
    """
    [문제 1] UART3로 "Hello World! {i}" 문자열을 1초마다 전송
    - 총 10번 전송 후 종료
    - 개행을 붙여 전송 (수신/테스트 편의)
    """

    port_name = "/dev/ttyAMA3"

    ser = Serial(
        port_name,
        baudrate=115200,
        timeout=1
    )

    for i in range(10):
        msg = f"Hello World! {i}\r\n"
        ser.write(msg.encode('utf-8'))
        print(f"전송: {msg.strip()}")
        time.sleep(1)

        ser.close()


def receive_msg() -> None:
    ser = Serial('/dev/ttyAMA3', baudrate=115200, timeout=1.0)

    buffer = ""
    while True:
        ch = ser.read().decode('utf-8', errors='ignore')
        if not ch:
            continue
        if ch == "\n":  # 한 줄 완성
            line = buffer.strip()
            if line:
                print(line)
                if line.lower() == "exit":
                    break
            buffer = ""
        else:
            buffer += ch

    ser.close()

if __name__ == "__main__":
    blink_led()
    check_to_input_button()
    blink_led_through_button()

    transmit_msg()
    receive_msg()
