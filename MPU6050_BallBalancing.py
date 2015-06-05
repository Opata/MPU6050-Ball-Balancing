#Added few more lines of codes to the previous project MPU_6050_Demo.py to move the ball on the line
#Balancing Ball with MPU6050 Demo on Raspberry pi 2 using ITG-MPU breakout board (MPU6050)
#This breakout board from aliexpress for $1.50. 40pin old IDE cable used to connect to raspi2
#no interrupt, +vcc of the board is connected to +5v of raspi2
#only sda, scl connected to raspi2.
#MPU data accessed regularly every 10ms (.01sec), sleep time reduced to allow data processing and draw.
#By Opata Padmasiri  
#codes for reading data from MPU6050 and complementrary filter taken from the following blog: 
#http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html

#!/usr/bin/python

import pygame, sys
from pygame.locals import *
import smbus
import math
import time  
pygame.init()
  
# set up the graphics window
screen = pygame.display.set_mode((800, 500), 0, 32)
pygame.display.set_caption('MPU_6050-Balancing Ball ')

#gem2.png image can be found in raspberry pi 2: " /home/pi/python_games"  folder.
ball = pygame.image.load("gem2.png")

  
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
  
# draw on the surface object
screen.fill(WHITE)
#==================================
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
gyro_scale = 131.0
accel_scale = 16384.0
 
address = 0x68  # This is the default I2C address of ITG-MPU breakout board

def read_all():
    raw_gyro_data = bus.read_i2c_block_data(address, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(address, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale
 
    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale
    
    return(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)
#==========================================================
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def dist(a, b):
    return math.sqrt((a * a) + (b * b))


bus = smbus.SMBus(1)  # SMBus(1) for Raspberry pi 2 board

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

now = time.time()
 
K = 0.98
K1 = 1 - K
time_diff = 0.01
(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

gyro_offset_x = gyro_scaled_x
gyro_offset_y = gyro_scaled_y

gyro_total_x = (last_x) - gyro_offset_x
gyro_total_y = (last_y) - gyro_offset_y
#========================
COLOR = RED
x0, y0 = 400,250 	# x0,y0 is the centre of the motion
xb, yb = 300,200  	#xb,yb is the start location of the ball
r = 250 			#radius of the circular motion
speed = 10			#speed of the ball

# run the loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        

    time.sleep(time_diff - 0.005)
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    
    gyro_scaled_x -= gyro_offset_x
    gyro_scaled_y -= gyro_offset_y
     
    gyro_x_delta = (gyro_scaled_x * time_diff)
    gyro_y_delta = (gyro_scaled_y * time_diff)

    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
 
    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
    
    #print last_x (X-angle),last_y (Y-angle) on terminal window
    print (last_x), (last_y)
    
    #x-coordinate of the ball depend on the angle & speed
    xb = xb - speed * last_y  
    
    angle_radian = math.radians(last_y)
    a = math.cos(angle_radian)
    b = math.sin(angle_radian)
    m = math.tan(angle_radian)    
 
    x1 = x0 - (r * a)
    y1 = y0 + (r * b)	
    x2 = x0 + (r * a)
    y2 = y0 - (r * b)
	
    #some maths to keep the ball on the line (y-coordinate)
    yb = (-m * (xb - x1) + y1)
    
    #drop the ball at the ends of the line
    if xb < x1: 
	yb = yb + 350 
	xb = x1 
    if xb > x2: 
	yb = yb + 350
	xb = x2
    		
    	
    screen.fill(WHITE) #clear window before redraw
    
    pygame.draw.line(screen, COLOR, (x1,y1), (x2,y2), 10) 
    
    screen.blit(ball, (xb-30,yb-60)) #off set to draw the ball on line
    

    pygame.display.update()
  
