# pip3 install pynput pyserial
import serial
from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as mController
import sys
import glob

superpresionado = False #si esta presionado este se suelta al momento de tocar otra tecla de forma que haga combinación
movermouse = False #cambia(si es verdadero las flechas mueven el mouse) el que se mueve al presionar las flechas(up,down,etc)

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
    0x00 : Key.cmd,      # Tecla super (0x5B)
    0x01 : Key.esc,      # Escape
    0x02 : Key.enter,    # Enter
    0x03 : Key.f11,      # Fullscreen
    0x04 : Key.page_up,  # Page up
    0x05 : Key.page_down,# Page down
    0x06 : Key.media_volume_up,     # volume +
    0x07 : Key.media_volume_down,   # volume -
    0x08 : Key.up,       # up arrow
    0x09 : Key.down,     # down arrow
    0x10 : Key.left,     # left arrow
    0x11 : Key.right,    # right arrow
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
mouse = mController()
print("Esperando datos")

try:
    while ser.is_open:
        if ser.in_waiting > 0:
            data = ser.read(1)  # Lee 1 byte crudo
            code = ord(data) if data else None
            print(code)
            if code in SPECIAL_KEYS:
                if movermouse == True and code == 0x08 or code == 0x09 or code == 0x10 or code == 0x11:
                    if code == 0x08:
                        mouse.move(0,10)
                    elif code == 0x09:
                        mouse.move(0,-10)
                    elif code == 0x10:
                        mouse.move(-10,0)
                    else:
                        mouse.move(10,0)
                else:
                    keyboard.press(SPECIAL_KEYS[code])
                    if code == 0x00:
                        superpresionado = True
                    else:
                        keyboard.release(SPECIAL_KEYS[code])
            else:
                # Si no es una tecla especial, intenta escribir el carácter
                try:
                    keyboard.press(chr(code))
                    keyboard.release(chr(code))
                    if superpresionado == True:
                        keyboard.release(Key.cmd)
                        superpresionado = False
                except:
                    print(f"Código no reconocido: {hex(code)}")
except KeyboardInterrupt:
    print("\nCerrando...")
finally:
    ser.close()
