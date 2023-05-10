import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

# GPIO pins for motor control
# Modify these pins according to your setup
enA_pin = 29
in1_pin = 31
in2_pin = 33
enB_pin = 36
in3_pin = 38
in4_pin = 40

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(enA_pin, GPIO.OUT)
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(enB_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)

# Function to control the motors
def control_motors(left_speed, right_speed):
    GPIO.output(in1_pin, GPIO.HIGH if left_speed > 0 else GPIO.LOW)
    GPIO.output(in2_pin, GPIO.HIGH if left_speed < 0 else GPIO.LOW)
    GPIO.output(in3_pin, GPIO.HIGH if right_speed > 0 else GPIO.LOW)
    GPIO.output(in4_pin, GPIO.HIGH if right_speed < 0 else GPIO.LOW)
    pwm_left.ChangeDutyCycle(abs(left_speed))
    pwm_right.ChangeDutyCycle(abs(right_speed))

# Function to get keyboard input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Main program
if __name__ == "__main__":
    try:
        # Set up PWM for motor speed control
        pwm_left = GPIO.PWM(enA_pin, 100)
        pwm_right = GPIO.PWM(enB_pin, 100)
        pwm_left.start(0)
        pwm_right.start(0)

        while True:
            char = getch()
            if char == "w":
                control_motors(50, 50)  # Forward with equal speed
            elif char == "s":
                control_motors(-50, -50)  # Backward with equal speed
            elif char == "a":
                control_motors(-50, 50)  # Turn left
            elif char == "d":
                control_motors(50, -50)  # Turn right
            elif char == "x":
                control_motors(0, 0)  # Stop
            elif char == "q":
                break

    except Exception as e:
        print(e)

    finally:
        # Clean up GPIO
        GPIO.cleanup()
