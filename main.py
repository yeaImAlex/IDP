import pygame
from motor import MotorControl
from camera import Webcam
from keyboard import Keyboard1
import threading
import time

# === Webcam Thread Handler ===
class CameraThread:
    def __init__(self):
        self.cam_thread = None
        self.running = False

    def start_camera(self):
        if not self.running:
            self.running = True
            self.cam_thread = threading.Thread(target=self.run_camera)
            self.cam_thread.start()

    def run_camera(self):
        cam = Webcam()
        cam.start()
        self.running = False  # Reset flag after camera window is closed

# === Main Control ===
def main():
    keyboard = Keyboard1()
    motor = MotorControl()
    cam_handler = CameraThread()

    try:
        print("?? Motor + Camera Control Started. Press 'E' to open camera. Press 'CTRL+C' to quit.")
        while True:
            if keyboard.getKey('w'):
                motor.move_forward(0.7)
            elif keyboard.getKey('s'):
                motor.move_backward(0.7)
            elif keyboard.getKey('a'):
                motor.turn_left(0.7)
            elif keyboard.getKey('d'):
                motor.turn_right(0.7)
            elif keyboard.getKey('e'):
                print("?? Launching camera...")
                cam_handler.start_camera()
            else:
                motor.stop_motor()

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("?? Stopped by user.")

    finally:
        motor.cleanup()
        pygame.quit()

if __name__ == "__main__":
    main()
