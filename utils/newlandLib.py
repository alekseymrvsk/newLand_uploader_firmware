import esptool
import serial

FIRMWARE_OFFSET = '0x10000'
SPIFFS_OFFSET = '0x290000'
uservector = 4
userkey = 20


# Генерирует пароль на основании ID устройства
# Аргументы str:id - ID устройства
# Возвращаемое значение: str - сгенерированный пароль
def generatePassword(devise_id: str) -> str:
    strlen = len(str(devise_id))
    mass = list(str(devise_id))
    for i in range(strlen):
        if int(mass[i]) + uservector < 10:
            mass[i] = str(int(mass[i]) + uservector)
    strmass = " ".join(mass)
    strmass = strmass.replace(" ", "")
    cryptKey = int(strmass)
    cryptKey = cryptKey * userkey
    cryptKey = int(str(cryptKey)[0:strlen])
    return str(cryptKey)


# Команда на загрузку файловой системы в устройство
# #Аргументы: port:str - имя последовательного порта к которму подключено устройство
#           baud:str - скорость работы порта при прошивке
#
def flashSPIFFS(port: str, baud: str):
    command = ['--chip', 'esp32', '--port', port, '--baud', baud, '--before', 'default_reset', 'write_flash', '-z',
               SPIFFS_OFFSET, 'spiffs.bin']
    esptool.main(command)


# Команда на загрузку прошивки в устройство
# #Аргументы: port:str - имя последовательного порта к которму подключено устройство
#           baud:str - скорость работы порта при прошивке
#  
def flashFirmware(port: str, baud: str):
    command = ['--chip', 'esp32', '--port', port, '--baud', baud, '--before', 'default_reset', '--after', 'hard_reset',
               'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '40m', '--flash_size', 'detect', '0x1000',
               'bootloader_dio_40m.bin', '0x8000', 'partitions.bin', '0xe000', 'boot_app0.bin', '0x10000',
               'firmware.bin']
    esptool.main(command)


# Запрос серийного номера устройства
# Аргументы: port - Serial порт к которому подключено устройство, порт должен быть открыт
#
# Возвращаемое значение: False - если порт не открыт, int:id - ID устройства в случае успешного захвата

def getSerialNum(port: serial.Serial):
    if (port.is_open):
        port.setDTR(1)
        linecount = 0
        id = None
        while linecount < 100:
            id = port.readline()
            if (b'$' in id and b'@' in id):
                print("ID захвачен")
                break
            else:
                linecount += 1

        if (id != None):
            return (int(id[1:-3].decode()))
        else:
            return False
    else:
        return False


# Команда на загрузку прошивки в устройство
# #Аргументы: port:str - имя последовательного порта к которму подключено устройство
#           baud:str - скорость работы порта при прошивке
#     
def eraseFlash(port: str, baud: str):
    command = ['--chip', 'esp32', '--port', port, '--baud', baud, '--before', 'default_reset', 'erase_flash']
    esptool.main(command)
