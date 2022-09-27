# MateBot
A bigger robot that is built around some small IKEA furniture.


## Todos

- Einbaumöglichkeit für:
	- Raspberry
	- Motor Treiber
- Stromversorgung Elektronik
- Software Motoren
- Treiber für Lidar
- Mount für Lidar
- Ultraschallsensoren

## Pin Setup

### Stepper Wiring

| Stepper | RST | SLP | STEP | DIR | M0 | M1 | M2 |
|-|-|-|-|-|-|-|-|
| Front Left | 3.3V | 2 | 3 | 4 | 7 | 8 | 25 |
| Front Right | 3.3V | 10 | 9 | 11 | 7 | 8 | 25 |
| Back Left | 3.3V | 13 | 19 | 26 | 7 | 8 | 25 |
| Back Right | 3.3V | 16 | 20 | 21 | 7 | 8 | 25 |

### Left Stepper

- RST:	3.3V (any)
- SLP:	GPIO 2
- STEP:	GPIO 3
- DIR:	GPIO 4
- GND:	GND (any)

### Right Stepper

- RST:	3.3V (any)
- SLP:	GPIO 10
- STEP:	GPIO 9
- DIR:	GPIO 11
- GND:	GND (any)