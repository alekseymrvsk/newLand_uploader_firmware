import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
import os.path
from design import uploader
from utils.newlandLib import eraseFlash, flashFirmware, flashSPIFFS, getSerialNum, generatePassword
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# TODO
# - Google API функция clientSicret выбор файла-токена через обзор и добавление id и пароля в таблицу


'''
Список всех кнопок в uploader.py:
- UploadButton
- EraseButton
- MakeFirmwareButton
- MakeFileSystemButton
- ClientSiret

Список всех полей:
- labelStatus
- labelPassword
- ClientSicret
- FirmfareLine
- FileSistemLine
- GoogleLine

Всплывающий список:
- ComPortComboBox
'''

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SPREADSHEET_ID = '1osUz0zxn7pscwX19GV3E6wNbfe_1MRKbV7EnDnxZH6U'
RANGE_NAME = 'A1:B'


def getPort(portName: str):
    for port in serial.tools.list_ports.comports():
        if port.name == portName:
            return port.name
        else:
            return None


def checkFile(filePath):
    if filePath.endswith('.bin') and os.path.exists(filePath):
        return True
    else:
        return False


class MyApp(QtWidgets.QMainWindow, uploader.Ui_MainWindow):
    pathFileFirmware = ''
    pathFileFileSystem = ''
    BAUD = '9600'  # Скорость работы порта

    def __init__(self):
        # Доступ к переменным, метода и т.д. в файле uploader.py
        super().__init__()
        self.token = None
        self.setupUi(self)  # Инициализация дизайна
        self.UploadButton.clicked.connect(self.upload)
        self.EraseButton.clicked.connect(self.erase)
        self.MakeFirmwareButton.clicked.connect(self.firmware)
        self.MakeFileSystemButton.clicked.connect(self.fileSystem)
        self.ClientSicret.clicked.connect(self.clientSicret)

    def clientSicret(self):
        self.token, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Files (*.json)')
        creds = Credentials.from_authorized_user_file(self.token, SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        response = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body={u'range': 'A1:B', u'values': [[u'id1', u'password1'], [u'id2', u'password2']],
                  u'majorDimension': u'ROWS'}).execute()

    def upload(self):
        portName = str(self.ComPortComboBox.currentText())
        port = serial.Serial(portName)
        eraseFlash(port=portName, baud=self.BAUD)
        flashFirmware(port=portName, baud=self.BAUD)
        flashSPIFFS(port=portName, baud=self.BAUD)

        deviceId = getSerialNum(port)
        generatePassword(deviceId)
        if deviceId is False:
            self.labelStatus.clear()
            self.labelPassword.clear()
            self.labelStatus.setStyleSheet("background-color: rgb(220,20,60);;\n"
                                           "border-radius:  10px;\n"
                                           "color:  rgb(220,20,60);")
            self.labelPassword.setStyleSheet("background-color: rgb(220,20,60);;\n"
                                             "border-radius:  10px;\n"
                                             "color:  rgb(220,20,60);")

    def erase(self):
        portName = str(self.ComPortComboBox.currentText())
        eraseFlash(port=portName, baud=self.BAUD)

    def firmware(self):
        self.pathFileFirmware, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Files (*.bin)')
        if checkFile(self.pathFileFirmware):
            self.FirmfareLine.setText(self.pathFileFirmware)
            self.MakeFileSystemButton.setEnabled(True)

    def fileSystem(self):
        self.pathFileFileSystem, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Files (*.bin)')
        if checkFile(self.pathFileFileSystem):
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
