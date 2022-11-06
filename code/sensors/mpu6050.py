'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
        http://www.electronicwings.com
'''
import smbus  # import SMBus module of I2C
import time
import math

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Full scale range +/- 250 degree/C as per sensitivity scale factor
MPU_SENSOR_GYRO_CONSTANT = 131.0
MPU_SENSOR_ACCEL_CONSTANT = 16384.0

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

# weight for the gyro angle for complementary filter 1-GYRO_WEIGHT is accel weight
GYRO_WEIGHT = 0.99


class mpu6050:

    def __init__(self):

        self.MPU_Init()
        self.gyro_x_drift = self.get_gyro_x_drift()
        self.gyro_y_drift = self.get_gyro_y_drift()
        self.gyro_z_drift = self.get_gyro_z_drift()
        self.accel_avg = self.get_accel_error()
        print('Gyro_Y_Drift:', self.gyro_y_drift,
              '| Accel_Avg:', self.accel_avg)
        self.gyro_angle = 0
        self.complementary_filter_angle = 0
        self.accel_angle = 0
        self.last_time = time.time()

    def MPU_Init(self):
        # write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        # Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        # Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        # Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        # Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        try:
            high = bus.read_byte_data(Device_Address, addr)
            low = bus.read_byte_data(Device_Address, addr+1)
        except Exception as ex:
            print(ex)
            print('Wrongly returning 0 from reading mpu6050 sensor data. Hoping robot will compensate wrong measurement in next iteration.')
            return 0

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if(value > 32768):
            value = value - 65536
        return value

    def get_new_gyro_angle(self, axis, time_diff_s, old_angle=0, raw_mode=False):
        gyro_drift = None
        DEGREE_SCALE_CONSTANT = 8
        if axis == 'x':
            raw = self.read_raw_data(GYRO_XOUT_H)
            gyro_drift = self.gyro_x_drift
        elif axis == 'y':
            raw = self.read_raw_data(GYRO_YOUT_H)
            gyro_drift = self.gyro_y_drift
        elif axis == 'z':
            raw = self.read_raw_data(GYRO_ZOUT_H)
            gyro_drift = self.gyro_z_drift

        if gyro_drift == None:
            if axis == 'x':
                gyro_drift = self.get_gyro_x_drift()
            elif axis == 'y':
                gyro_drift = self.get_gyro_y_drift()
            elif axis == 'z':
                gyro_drift = self.get_gyro_z_drift()

        raw = raw / MPU_SENSOR_GYRO_CONSTANT
        raw = (raw-gyro_drift) * DEGREE_SCALE_CONSTANT

        if raw_mode:
            return raw

        angle = old_angle + (raw * time_diff_s)
        return angle

    def get_new_accel_angle(self, axis, initial_angle=0):
        if axis == 'x':
            raw = self.read_raw_data(ACCEL_XOUT_H)
        elif axis == 'y':
            raw = self.read_raw_data(ACCEL_YOUT_H)
        elif axis == 'z':
            raw = self.read_raw_data(ACCEL_ZOUT_H)
        raw = raw / MPU_SENSOR_ACCEL_CONSTANT

        angle = raw * 180 + 180 - initial_angle

        return angle

    def get_full_accel_data(self):
        try:
            x = self.read_raw_data(ACCEL_XOUT_H)/MPU_SENSOR_ACCEL_CONSTANT
            y = self.read_raw_data(ACCEL_YOUT_H)/MPU_SENSOR_ACCEL_CONSTANT
            z = self.read_raw_data(ACCEL_ZOUT_H)/MPU_SENSOR_ACCEL_CONSTANT
        except:
            return self.get_full_accel_data()
        return (x, y, z)

    def dotproduct(self, v1, v2):
        return sum((a*b) for a, b in zip(v1, v2))

    def length(self, v):
        return math.sqrt(self.dotproduct(v, v))

    def angle(self, v1, v2):
        try:
            result = math.acos(self.dotproduct(v1, v2) /
                               (self.length(v1) * self.length(v2)))
        except:
            return 0
        return result

    def get_accel_error(self, samples=100):
        return sum([math.degrees(self.angle(self.get_full_accel_data(), (1, 0, 0))) for i in range(samples)])/samples

    def get_gyro_x_drift(self, samples=100):
        return sum([self.read_raw_data(GYRO_XOUT_H)/MPU_SENSOR_GYRO_CONSTANT for i in range(samples)])/samples

    def get_gyro_y_drift(self, samples=100):
        return sum([self.read_raw_data(GYRO_YOUT_H)/MPU_SENSOR_GYRO_CONSTANT for i in range(samples)])/samples

    def get_gyro_z_drift(self, samples=100):
        return sum([self.read_raw_data(GYRO_ZOUT_H)/MPU_SENSOR_GYRO_CONSTANT for i in range(samples)])/samples

    def get_angle(self):
        '''
        Simply call this function in a loop to get angles.
        Output:
        [0] = angle from complementary filter
        [1] = angle from gyro
        [2] = angle from accel
        [3] = Sampling frequency
        '''
        curr_time = time.time()
        time_diff = curr_time - self.last_time
        self.last_time = curr_time

        gyro_raw = self.get_new_gyro_angle(
            'y', time_diff, self.gyro_y_drift, 0,  True)

        accel_raw = self.get_full_accel_data()

        accel_dir = 1 if accel_raw[2] > 0 else -1

        self.gyro_angle = self.gyro_angle + gyro_raw * time_diff
        self.accel_angle = (math.degrees(self.angle(
            accel_raw, (1, 0, 0))) - self.accel_avg) * accel_dir

        self.complementary_filter_angle = (
            GYRO_WEIGHT * (self.complementary_filter_angle + gyro_raw * time_diff)) + ((1-GYRO_WEIGHT)*self.accel_angle)

        freq = 1 / time_diff
        return (self.complementary_filter_angle, self.gyro_angle, self.accel_angle, freq)