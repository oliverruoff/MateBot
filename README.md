# MateBot
A bigger robot that is built around some small IKEA furniture.


## Wiring

- gpio_mode=GPIO.BCM
- All pin declarations are like "GPIO123"

### Drive Steppers

| Stepper |ENA | DIR | STEP |
|-|-|-|-|
| Front Left | 26 | 11 | 9 |
| Front Right | 26 | 10 | 22 |
| Back Left | 26 | 19 | 13 |
| Back Right | 26 | 6 | 5 |

### Lidar Stepper

| SLP | DIR | STEP |
|-|-|-|
| 21 | 16 | 20 |

### Lidar

>TODO

### Sonic Sensors

>TODO

### CJMCU-219 INA219 Voltage / Current Meter

| SDA | SCL |
|-|-|
| 2 | 3 | 

### MPU6050 Gyroscope / Acceleration Sensor

>TODO