from time import sleep
import threading

import RPi.GPIO as GPIO
import pigpio

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation

# For microstepping
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4':  (0, 1, 0),
              '1/8':  (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

class stepper:
    """This class is for handling the DRV8825 motor driver. E.g. to operate
        common bigger stepper motors.
        """

    def __init__(self, DIR, STEP, SLP, steps_per_revolution, M0=None, M1=None, M2=None, RST=None, step_mode='Full', step_delay_seconds=.005, activate_on_high=True, gpio_mode=GPIO.BCM):
        self.DIR = DIR
        self.STEP = STEP
        self.RST = RST
        self.M0 = M0
        self.M1 = M1
        self.M2 = M2
        self.step_mode = step_mode
        # If set to Low, there is no holding torque on the motor
        self.SLP = SLP
        # Steps per Revolution (360 / 1.8) (1,8° per step (oruoff))
        self.steps_per_revolution = steps_per_revolution

        self.step_delay_seconds = step_delay_seconds
        self.activate_on_high = activate_on_high
        self.gpio_mode = gpio_mode

        self.pi = pigpio.pi()

        self.direction = CW

        GPIO.setmode(gpio_mode)

        if RST is not None:
            GPIO.setup(self.RST, GPIO.OUT)
            GPIO.output(self.RST, GPIO.HIGH)

        if M0 is not None:
            GPIO.setup(self.M0, GPIO.OUT)

        if M1 is not None:
            GPIO.setup(self.M1, GPIO.OUT)

        if M2 is not None:
            GPIO.setup(self.M2, GPIO.OUT)

        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.SLP, GPIO.OUT)

        GPIO.output(DIR, CW)

    def set_step_delay(self, step_delay_seconds):
        """Sets the delay in seconds for the driver to wait between steps.

        Args:
            step_delay_seconds (float): Delay in seconds to wait between steps.
        """
        self.step_delay_seconds = step_delay_seconds

    def activate(self):
        """Activates the stepper, which also will put holding torque on the stepper.
        This is required in order to move the stepper.
        """
        if self.activate_on_high:
            GPIO.output(self.SLP, GPIO.HIGH)
        else:
            GPIO.output(self.SLP, GPIO.LOW)

    def deactivate(self):
        """Deactivates the stepper and also releases holding torque on the stepper.
        In a deactivated state, the stepper will not be able to move.
        """
        if self.activate_on_high:
            GPIO.output(self.SLP, GPIO.LOW)
        else:
            GPIO.output(self.SLP, GPIO.HIGH)

    def set_step_mode(self, mode):
        """Sets the stepper mode to one of 'Full', 'Half', '1/4', '1/8', '1/16', '1/32'.
        Next usage of the stepper will take this stepper mode.

        Args:
            mode (str): Stepper mode. One of ['Full', 'Half', '1/4', '1/8', '1/16', '1/32']
        """
        self.step_mode = mode
        if None in [self.M0, self.M1, self.M2]:
            print('M0, M1, or M2 not defined! ->', [self.M0, self.M1, self.M2], '. Mode set though.')
        else:
            self.pi.write(self.M0, RESOLUTION[mode][0])
            self.pi.write(self.M1, RESOLUTION[mode][1])
            self.pi.write(self.M2, RESOLUTION[mode][2])

    def run_continuously(self, dutycycle=128, frequency=8000):
        """Activated, the stepper will continuously run with the desired frequency.
        The dutycycle describes the distribution of high low states, where 128 is 50% / 50% high / low.

        Args:
            dutycycle (int, optional): Describes high / low ratio. 128 is 50%/50%. Defaults to 128.
            frequency (int, optional): Describes the frequency of the stepper's high / low states. Defaults to 320.
            Can be: 320 / 400 / 500 / 800 / 1000 / 1600 / 2000 / 4000 / 8000
        """
        self.activate()
        self.pi.set_PWM_dutycycle(self.STEP, dutycycle)
        self.pi.set_PWM_frequency(self.STEP, frequency)

    def stop_continuous(self):
        """Stops the continuous turning of the stepper. Also deactivates it, thus
        releasing holding torque.
        """
        self.deactivate()
        self.pi.set_PWM_dutycycle(self.STEP, 0)

    def set_direction_clockwise(self, clockwise=True):
        """Sets the spinning direction of the stepper motor to clockwise or
        counterclockwise.

        Args:
            clockwise (bool, optional): Spinning direction. Defaults to True.
        """
        self.direction = CW if clockwise else CCW
        GPIO.output(self.DIR, self.direction)

    def is_direction_clockwise(self):
        """Returns True if the current direction set is clockwise, else False.

        Returns:
            bool: True if clockwise, else False.
        """
        return bool(self.direction)

    def turn_angle(self, degree, asynch, ramping=False):
        """Turns the stepper for a precise angle. Can be called
        either synchronous or asynchronously. Stepper mode is respected.

        Args:
            degree (int): The angle in degree, on how much the stepper will
            rotate.
            asynch (bool): Flag wheather this function (and therefore the motor), will turn
            synchronously or asynchronously.
        """
        if (asynch):
            thread = threading.Thread(
                target=self._turn_stepper, args=([degree, ramping]), kwargs={})
            thread.start()
        else:
            self._turn_stepper(degree, ramping)

    def _ramping_function(self, current_step, all_steps):
        """Uses a defined exponential function to output the y value, which can be used
        as delay for the stepper

        Args:
            current_step (int): The current step number (iteratively increased)
            all_steps (int): The number of all steps for the current movement.

        Returns:
            float: The resulting y value, which can be used as stepper delay in seconds.
        """
        X_AXIS_SHIFT = -0.004
        GRAPH_WIDTH = abs(2*X_AXIS_SHIFT)
        EXPONENT = 2
        PARABOLA_SHARPNESS = 1000000
        x = GRAPH_WIDTH/all_steps*current_step
        y = PARABOLA_SHARPNESS*pow(x+X_AXIS_SHIFT, EXPONENT) * \
            self.step_delay_seconds + self.step_delay_seconds
        return y

    def _get_stepper_multiplier_from_mode(self):
        """Checks current self.step_mode and returns multiplier for it, which is used to 
        get the required number of steps to turn for a specific angle.

        Returns:
            int: Multiplier which is multiplied with steps required for microstepping a specific angle.
        """
        stepper_mode_multiplier = -1
        if self.step_mode == 'Full':
            stepper_mode_multiplier = 1
        elif self.step_mode == 'Half':
            stepper_mode_multiplier = 2
        elif self.step_mode == '1/4':
            stepper_mode_multiplier = 4
        elif self.step_mode == '1/8':
            stepper_mode_multiplier = 8
        elif self.step_mode == '1/16':
            stepper_mode_multiplier = 16
        elif self.step_mode == '1/32':
            stepper_mode_multiplier = 32
        else:
            print('Failed to get stepper mode multiplier!')
            return None
        return stepper_mode_multiplier

    def get_steps_for_angle(self, degree):
        """Can be used to get the steps to turn the stepper for a certain angle.
        Microstepping is respected, using function `_get_stepper_multiplier_from_mode()`.

        Args:
            degree (int): Angle in degree which the stepper should turn

        Returns:
            int: Number of steps that have to be taken.
        """
        stepper_mode_multiplier = self._get_stepper_multiplier_from_mode()
        return int(self.steps_per_revolution/360*degree) * stepper_mode_multiplier

    def _turn_stepper(self, degree, ramping=False):
        """This function is for turning the stepper for a precise angle.
        This function should be called with the `turn_stepper_angle` function,
        defining whether the function should run synchronously or asynchronously.

        Args:
            degree (int): The angle in degree, on how much the stepper will rotate.
            ramping (bool): Defines wheather the stepper should ramp up and down its movement.
        """
        self.activate()
        stepper_mode_multiplier = self._get_stepper_multiplier_from_mode()

        steps = int(self.steps_per_revolution/360*degree) * stepper_mode_multiplier
        for i in range(steps):
            if ramping:
                delay = self._ramping_function(i, steps)
            else:
                delay = self.step_delay_seconds
            self.step_high()
            sleep(delay)
            self.step_low()
            sleep(delay)

    def step_high(self):
        """Can be used to put high signal on stepper.
        """
        GPIO.output(self.STEP, GPIO.HIGH)

    def step_low(self):
        """Can be used to put low signal on stepper.
        """
        GPIO.output(self.STEP, GPIO.LOW)

    def make_one_step(self):
        """Executes exactly one full step.
        """
        self.activate_stepper()
        self.step_high()
        sleep(self.step_delay_seconds)
        self.step_low()
        sleep(self.step_delay_seconds)