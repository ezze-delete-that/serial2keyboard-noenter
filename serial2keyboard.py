# pip3 install pynput pyserial
import serial
from pynput.keyboard import Key, Controller
import sys
import glob

enterpresionado = False

def list_ports():
    """ Lista todos los puertos seriales disponibles """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, Exception):
            pass
    return result

# Mapeo de códigos ASCII a teclas especiales (pynput.Key)
SPECIAL_KEYS = {
    0x5B: Key.cmd,      # Tecla Windows (0x5B)
    0x1B: Key.esc,      # Escape
    0x0D: Key.enter,    # Enter
    # Agrega más códigos aquí según lo necesites
}

if len(sys.argv) < 2:
    print("Uso: python3 serial2keyboard.py [Puerto] [BaudRate opcional]")
    print("Puertos detectados:", list_ports())
    sys.exit(1)

baudRate = 9600 if len(sys.argv) < 3 else int(sys.argv[2])
print(f"Abriendo {sys.argv[1]} a {baudRate} bauds")

try:
    ser = serial.Serial(sys.argv[1], baudRate, timeout=1)
except Exception as e:
    print(f"Error al abrir el puerto: {e}")
    sys.exit(1)

keyboard = Controller()

print("Esperando datos (envía códigos ASCII crudos, ej: 0x5B para Win)...")

try:
    while ser.is_open:
        if ser.in_waiting > 0:
            data = ser.read(1)  # Lee 1 byte crudo
            code = ord(data) if data else None
            
            if code in SPECIAL_KEYS:
                keyboard.press(SPECIAL_KEYS[code])
                if code == 0x5B:
                    enterpresionado = True
                else:
                    keyboard.release(SPECIAL_KEYS[code])
            else:
                # Si no es una tecla especial, intenta escribir el carácter
                try:
                    keyboard.press(chr(code))
                    keyboard.release(chr(code))
                    keyboard.release(Key.cmd)
                    enterpresionado = False
                except:
                    print(f"Código no reconocido: {hex(code)}")
except KeyboardInterrupt:
    print("\nCerrando...")
finally:
    ser.close()
