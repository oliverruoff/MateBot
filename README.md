# MateBot
A bigger robot that is built around some small IKEA furniture.


## Wiring

- gpio_mode=GPIO.BCM
- All pin declarations are like "GPIO123"

### Drive Steppers

> Those stepper drivers activate by setting ENA pin to LOW

| Stepper |ENA | DIR | STEP |
|-|-|-|-|
| Front Left | 26 | 11 | 9 |
| Front Right | 26 | 10 | 22 |
| Back Left | 26 | 19 | 13 |
| Back Right | 26 | 6 | 5 |

### Lidar Stepper

> This stepper driver activate by setting SLP pin to HIGH

| SLP | DIR | STEP |
|-|-|-|
| 21 | 16 | 20 |

### Lidar

| RXD/SDA | TXT/SCL |
|-|-|
| 15 | 14 |

### CJMCU-219 INA219 Voltage / Current Meter

| SDA | SCL |
|-|-|
| 2 | 3 | 

### MPU6050 Gyroscope / Acceleration Sensor

| SDA | SCL |
|-|-|
| 2 | 3 | 