from board import board_info
from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO
from time import sleep

test_pin=16
fpioa = FPIOA()
fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.IN)
lcd.init(color=(255,0,0))
lcd.draw_string(100,120, "Welcome to MaixPy", lcd.WHITE, lcd.RED)
if test_gpio.value() == 0:
    print('PIN 16 pulled down, enter test mode')
    import sensor
    import image
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    lcd.freq(16000000)
    while True:
        img=sensor.snapshot()
        lcd.display(img)

sleep(2)

#refer to http://blog.sipeed.com/p/675.html
import sensor
import image
import lcd
import KPU as kpu

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
task = kpu.load(0x300000) # you need put model(face.kfpkg) in flash at address 0x300000
# task = kpu.load("/sd/face.kmodel")
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            print(i)
            a = img.draw_rectangle(i.rect())
            lcd.draw_string(150,20, "CAUTION!!", lcd.WHITE, lcd.RED)
            # img.draw_string(100,20, "CAUTION!!", color=(256,0,0), scale=2)
            # img.draw_string(0,20, "CAUTION!!", color=(256,0,0), scale=4)
            sleep(1)
    a = lcd.display(img)
a = kpu.deinit(task)