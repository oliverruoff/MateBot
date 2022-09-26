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
| Front Left | b | c | d | e |
| Front Right | 3.3V | 10 | 9 | 11 | 7 | 8 | 25 |
| Back Left | b | c | d | e |
| Back Right | b | c | d | e |

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