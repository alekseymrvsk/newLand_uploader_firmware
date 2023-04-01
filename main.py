import sys

import serial.tools.list_ports
from PyQt5 import QtWidgets

from design import uploader
from utils.newlandLib import eraseFlash, flashFirmware, flashSPIFFS, getSerialNum, generatePassword

# TODO:
# - добавить выбор com-порта
# - запуск команд из newLandLib.py по загрузке прошивки


'''
Список всех кнопок в uploader.py:
- UploadButton
- EraseButton
- MakeFirmwareButton
- MakeFileSystemButton

Список всех полей:
- labelStatus
- labelPassword
- ClientSicret
- FirmfareLine
- FileSistemLine

Всплывающий список:
- ComPortComboBox
'''


def getPort(portName: str):
    for port in serial.tools.list_ports.comports():
        if port.name == portName:
            return port
        else:
            return None


class MyApp(QtWidgets.QMainWindow, uploader.Ui_MainWindow):
    pathFileFirmware = ''
    pathFileFileSystem = ''
    BAUD = '115200'  # Скорость работы порта

    def __init__(self):
        # Доступ к переменным, метода и т.д. в файле uploader.py
        super().__init__()
        self.setupUi(self)  # Инициализация дизайна
        self.UploadButton.clicked.connect(self.upload)
        self.EraseButton.clicked.connect(self.erase)
        self.MakeFirmwareButton.clicked.connect(self.firmware)
        self.MakeFileSystemButton.clicked.connect(self.fileSystem)

    def upload(self):
        portName = str(self.ComPortComboBox.currentText())
        port = getPort(portName)

        eraseFlash(port=portName, baud=self.BAUD)
        flashFirmware(port=portName, baud=self.BAUD)
        flashSPIFFS(port=portName, baud=self.BAUD)
        deviceId = getSerialNum(port)
        generatePassword(deviceId)

    def erase(self):
        pass

    def firmware(self):
        self.pathFileFirmware, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Files (*.bin)')
        if self.pathFileFirmware:
            self.FirmfareLine.setText(self.pathFileFirmware)
            self.MakeFileSystemButton.setEnabled(True)

    def fileSystem(self):
        self.pathFileFileSystem, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Files (*.bin)')
        if self.pathFileFileSystem:
            self.FileSistemLine.setText(self.pathFileFileSystem)
            self.EraseButton.setEnabled(True)
            self.UploadButton.setEnabled(True)
            self.ClientSicret.setEnabled(True)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
