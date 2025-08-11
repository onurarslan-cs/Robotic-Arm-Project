import cv2
import numpy as np
import serial
import time

# Arduino'nun bağlı olduğu portu belirt
arduino_port = 'COM3'
baud_rate = 9600

# Seri bağlantıyı başlat
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Bağlantının oturması için kısa bir süre bekle

# Robot kolun belirli konumları (örnek olarak)
pickup_position2 = [0, 20, 60, 120, 105, 150]
pickup_position1 = [0, 90, 90, 120, 90, 150]
home_position = [90, 90, 90, 120, 90, 100]
home_position2 = [90, 90, 90, 120, 90, 0]
drop_positions = {
   'red': [120, 50, 70, 120, 45, 150],
   'green': [140, 70, 90, 120, 60, 150],
   'blue': [155, 80, 90, 120, 45, 150]
}

def move_to_position(position, step_delay):
    command = f"MOVE {position[0]:03d} {position[1]:03d} {position[2]:03d} {position[3]:03d} {position[4]:03d} {position[5]:03d} {step_delay}\n"
    ser.write(command.encode())
    time.sleep(step_delay * len(position) / 10)  # Hareketin tamamlanması için bekleme süresi

def close_gripper():
    ser.write("CLOSE_GRIPPER\n".encode())
   #time.sleep(1)  # Gripper kapatma süresi


def open_gripper():
    ser.write("OPEN_GRIPPER\n".encode())
    time.sleep(1)  # Gripper açma süresi

# Kamera ile renk algılama
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızı renk için HSV aralığı
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_red = mask1 + mask2

    # Yeşil renk için HSV aralığı
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Mavi renk için HSV aralığı
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    red_detected = np.sum(mask_red)
    green_detected = np.sum(mask_green)
    blue_detected = np.sum(mask_blue)

    step_delay = 20

    if red_detected > 10000:  # Kırmızı renk algılandıysa
        move_to_position(pickup_position1, step_delay)  # Alım pozisyonuna git
        move_to_position(pickup_position2, step_delay)  # Alım pozisyonuna git
        close_gripper()  # Gripper kapat
        time.sleep(3)
        move_to_position(home_position2, step_delay)  # Ev pozisyonuna dön
        move_to_position(drop_positions['red'], step_delay)  # Kırmızı hedef pozisyonuna git
        open_gripper()  # Gripper aç
        move_to_position(home_position, step_delay)  # Başlangıç pozisyonuna dön
    elif green_detected > 10000:  # Yeşil renk algılandıysa
        move_to_position(pickup_position1, step_delay)  # Alım pozisyonuna git
        move_to_position(pickup_position2, step_delay)  # Alım pozisyonuna git

        close_gripper()  # Gripper kapat
        time.sleep(3)
        move_to_position(home_position2, step_delay)  # Ev pozisyonuna dön
        move_to_position(drop_positions['green'], step_delay)  # Yeşil hedef pozisyonuna git
        open_gripper()  # Gripper aç
        move_to_position(home_position, step_delay)  # Başlangıç pozisyonuna dön
    elif blue_detected > 10000:  # Mavi renk algılandıysa
        move_to_position(pickup_position1, step_delay)  # Alım pozisyonuna git
        move_to_position(pickup_position2, step_delay)  # Alım pozisyonuna git
        close_gripper()  # Gripper kapat
        time.sleep(3)
        move_to_position(home_position2, step_delay)  # Ev pozisyonuna dön
        move_to_position(drop_positions['blue'], step_delay)  # Mavi hedef pozisyonuna git
        open_gripper()  # Gripper aç
        move_to_position(home_position, step_delay)  # Başlangıç pozisyonuna dön

    cv2.imshow('Frame', frame)
    cv2.imshow('Red Mask', mask_red)
    cv2.imshow('Green Mask', mask_green)
    cv2.imshow('Blue Mask', mask_blue)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
