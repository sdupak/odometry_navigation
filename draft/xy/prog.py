#!/usr/bin/env python3
from ev3dev.ev3 import *
import math

k1 = 15
k2 = 5
array = [[0.4, 0.4], [-0.4, 0.4], [-0.4, -0.4], [0.4, -0.4], [0.4, 0.4]]
voltage = 7.00
r = 0.02
B = 0.12
ok_zone = 0.05

mA = LargeMotor('outA')
mB = LargeMotor('outB')
fh = open('data_' + str(k1) + '-' + str(k2) + '.txt', 'w')

desired_x = array[0][0]
desired_y = array[0][1]
current_x = 0
current_y = 0
complite = 0
mA.position = 0
mB.position = 0
prev_path = 0

try:
    while complite < len(array):
        motorA_pos = mA.position * math.pi / 180
        motorB_pos = mB.position * math.pi / 180
        path = (motorA_pos+motorB_pos)*(r/2)
        dpath = path - prev_path
        prev_path = path
        current_angle = (motorA_pos - motorB_pos)*(r/B)
        current_x += dpath*math.cos(current_angle)
        current_y += dpath*math.sin(current_angle)
        dx = desired_x - current_x
        dy = desired_y - current_y
        path_err = math.sqrt(dx**2 + dy**2)
        need_angle = math.atan2(dy, dx)
        angle_err = need_angle - current_angle
        if abs(angle_err) > math.pi:
            angle_err -= math.copysign(1, angle_err)*2*math.pi
        u_straight = k1*path_err
        u_rotation = k2*angle_err
        sA = u_straight + u_rotation
        sB = u_straight - u_rotation
        sA = sA * 100 / voltage
        sB = sB * 100 / voltage
        if abs(sA) > 100:
            sA = math.copysign(100, sA)
        if abs(sB) > 100:
            sB = math.copysign(100, sB)    
        mA.run_direct(duty_cycle_sp=sA)
        mB.run_direct(duty_cycle_sp=sB)
        mystr = str(current_x) + ' ' + str(current_y) + ' '
        mystr += str(current_angle) + ' ' + str(time.time()) + '\n \n'
        fh.write(mystr)
        if (abs(dx) < ok_zone) and (abs(dy) < ok_zone):
            complite += 1
            if complite < len(array):
                desired_x = array[complite][0]
                desired_y = array[complite][1]
finally:
    mA.stop(stop_action='brake')
    mB.stop(stop_action='brake')
    fh.close
