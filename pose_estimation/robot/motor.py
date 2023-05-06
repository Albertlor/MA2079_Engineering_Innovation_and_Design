import time
import RPi.GPIO as GPIO
import curses


class Motor():
    def __init__(self, ENA, IN1, IN2, ENB, IN3, IN4):
        """
        Initialize the GPIO pins
        """
        self.ENA = ENA
        self.IN1 = IN1
        self.IN2 = IN2
        self.ENB = ENB
        self.IN3 = IN3
        self.IN4 = IN4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)

        # Speed of the motors
        speed = 0

        # Set up PWM for motor control
        self.pwm_a = GPIO.PWM(self.ENA, 100)
        self.pwmA.start(speed)
        self.pwm_b = GPIO.PWM(self.ENB, 100)
        self.pwmB.start(speed)

    # Motor control functions
    def forward():
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)

    def backward():
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)

    def left():
        GPIO.output(IN1, True)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, True)

    def right():
        GPIO.output(IN1, False)
        GPIO.output(IN2, True)
        GPIO.output(IN3, True)
        GPIO.output(IN4, False)

    def stop():
        GPIO.output(IN1, False)
        GPIO.output(IN2, False)
        GPIO.output(IN3, False)
        GPIO.output(IN4, False)

def movement(stdscr):
    # Clear the screen and set up the curses environment
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(True)

    # Loop until the user presses the Escape key
    while True:
        # Wait for user input
        key = stdscr.getch()
        #, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN
        # Check if the user pressed an arrow key
        if key in [curses.KEY_LEFT]:
            motor.left()
        elif key in [curses.KEY_RIGHT]:
            motor.right()
        elif key in [curses.KEY_UP]:
            motor.forward()
        elif key in [curses.KEY_DOWN]:
            motor.backward()
        # Check if the user pressed the Escape key
        elif key == 27:
            break
        else: 
            motor.stop()

        # Refresh the screen
        stdscr.refresh()

if __name__ == '__main__':
    #set up IO pins
    ENA = 29
    IN1 = 31
    IN2 = 33
    IN3 = 36
    IN4 = 38
    ENB = 40
    motor = Motor(ENA, IN1, IN2, ENB, IN3, IN4)

    # Set up the curses environment and run the main function
    curses.wrapper(movement)

    # Cleanup GPIO pins
    GPIO.cleanup()
