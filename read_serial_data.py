import os
import django
import serial
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panel_solar.settings')
django.setup()

from datos_arduino.models import SensorData

# Ajusta el puerto y la velocidad (baudrate) según tu Arduino
SERIAL_PORT = 'COM3'  # Cambia esto a tu puerto, ejemplo: 'COM4', '/dev/ttyACM0' (Linux)
BAUD_RATE = 9600

pattern = re.compile(
    r'LDR_Left_Top: (\d+), LDR_Right_Top: (\d+), LDR_Left_Bottom: (\d+), LDR_Right_Bottom: (\d+), Solar_Value: (\d+)'
)

def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Escuchando datos del Arduino...")
        while True:
            line = ser.readline().decode('latin1').strip()
            if line:
                match = pattern.match(line)
                if match:
                    ldr_lt = int(match.group(1))
                    ldr_rt = int(match.group(2))
                    ldr_lb = int(match.group(3))
                    ldr_rb = int(match.group(4))
                    solar = int(match.group(5))

                    SensorData.objects.create(
                        ldr_left_top=ldr_lt,
                        ldr_right_top=ldr_rt,
                        ldr_left_bottom=ldr_lb,
                        ldr_right_bottom=ldr_rb,
                        solar_value=solar
                    )
                    print(f"Guardado: {ldr_lt}, {ldr_rt}, {ldr_lb}, {ldr_rb}, {solar}")

if __name__ == '__main__':
    main()
