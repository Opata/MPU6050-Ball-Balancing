# MPU6050-Ball-Balancing
Ball Balancing with MPU6050 on Raspberry Pi 2 using ITG-MPU breakout board (MPU6050). This breakout board from aliexpress for $1.50. 40pin old IDE cable used to connect to raspi2 no interrupt, +vcc of the board is connected to +5v of raspi2 only sda, scl connected to raspi2. MPU data accessed regularly every 10ms (.01sec), sleep time reduced to allow data processing and draw. 
Codes for reading data from MPU6050 and complementary filter taken from the following blog: http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html.
You can find the  gem2.png image in /home/pi/python_games/gem2.png  directory of Raspberry Pi 2.
