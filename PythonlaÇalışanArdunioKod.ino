#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

int currentPos1 = 90;
int currentPos2 = 90;
int currentPos3 = 90;
int currentPos4 = 120;
int currentPos5 = 90;
int currentPos6 = 100;

void setup() {
  Serial.begin(9600);
  servo1.attach(31);
  servo2.attach(33);
  servo3.attach(35);
  servo4.attach(37);
  servo5.attach(41);
  servo6.attach(39);

  // Servoları başlangıç pozisyonuna ayarla
  servo1.write(currentPos1);
  servo2.write(currentPos2);
  servo3.write(currentPos3);
  servo4.write(currentPos4);
  servo5.write(currentPos5);
  servo6.write(currentPos6);
}

void moveToPosition(int pos1, int pos2, int pos3, int pos4, int pos5, int pos6, int stepDelay) {
  while (currentPos1 != pos1 || currentPos2 != pos2 || currentPos3 != pos3 || currentPos4 != pos4 || currentPos5 != pos5 || currentPos6 != pos6) {
    if (currentPos1 < pos1) currentPos1++;
    else if (currentPos1 > pos1) currentPos1--;
    
    if (currentPos2 < pos2) currentPos2++;
    else if (currentPos2 > pos2) currentPos2--;
    
    if (currentPos3 < pos3) currentPos3++;
    else if (currentPos3 > pos3) currentPos3--;
    
    if (currentPos4 < pos4) currentPos4++;
    else if (currentPos4 > pos4) currentPos4--;
    
    if (currentPos5 < pos5) currentPos5++;
    else if (currentPos5 > pos5) currentPos5--;
    
    if (currentPos6 < pos6) currentPos6++;
    else if (currentPos6 > pos6) currentPos6--;
    
    servo1.write(currentPos1);
    servo2.write(currentPos2);
    servo3.write(currentPos3);
    servo4.write(currentPos4);
    servo5.write(currentPos5);
    servo6.write(currentPos6);
    
    delay(stepDelay);
  }
}

void closeGripper() {
  servo6.write(0); // Gripper kapat
 
}

void openGripper() {
  servo6.write(150); // Gripper aç
  delay(1000); // Gripper açma süresi
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("MOVE")) {
      int pos1 = command.substring(5, 8).toInt();
      int pos2 = command.substring(9, 12).toInt();
      int pos3 = command.substring(13, 16).toInt();
      int pos4 = command.substring(17, 20).toInt();
      int pos5 = command.substring(21, 24).toInt();
      int pos6 = command.substring(25, 28).toInt();
      
      moveToPosition(pos1, pos2, pos3, pos4, pos5, pos6, 50); // Daha uzun bir gecikme süresi (ms)
    } else if (command.startsWith("CLOSE_GRIPPER")) {
      closeGripper(); // Gripper kapat
    } else if (command.startsWith("OPEN_GRIPPER")) {
      openGripper(); // Gripper aç
    }
  }
}
