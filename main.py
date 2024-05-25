import cv2
import numpy as np

class HomeDefender:
    def __init__(self):
        self.alarm_on = False
        self.camera_index = 0
        self.cap = cv2.VideoCapture(self.camera_index)
        self.alarm_triggered = False

    def turn_alarm_on(self):
        self.alarm_on = True
        print("Alarm is now ON.")

    def turn_alarm_off(self):
        self.alarm_on = False
        self.alarm_triggered = False
        print("Alarm is now OFF.")

    def detect_movement(self):
        ret, frame1 = self.cap.read()
        ret, frame2 = self.cap.read()
        
        if not ret:
            print("Failed to grab frames.")
            return

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue
            if self.alarm_on:
                self.trigger_alarm()
                break

    def trigger_alarm(self):
        if not self.alarm_triggered:
            print("Movement detected! Alarm is ringing!")
            self.alarm_triggered = True

    def run(self):
        try:
            while True:
                self.detect_movement()
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    defender = HomeDefender()
    defender.turn_alarm_on()
    defender.run()
