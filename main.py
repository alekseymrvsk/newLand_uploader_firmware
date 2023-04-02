from __future__ import print_function

import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
import os.path
from design import uploader
from utils.newlandLib import eraseFlash, flashFirmware, flashSPIFFS, getSerialNum, generatePassword
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
                     !!!!!!!!!!!!!!!!!!!!!!!!!
Добавление данных в гугл-таблицу должно быть в методе upload и 
срабатывать после нажатия на кнопку Upload и после прошивки, 
но для демонстрации работы кода данный функционал перенесен в метод clientService, т.к. нет целевого контроллера, т.е.
нет ID и пароля для добавления в таблицу.
В таблицу добавляются константные значения

Время от времени токен(token.json) становится не действительным. Нужно удалить его и запустить приложение. При нажатии 
на кнопку ClientSicret после авторизации сгенерируется новый токен
'''

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


# Проверка файлов прошивки и файловой системы
def checkFile(filePath):
    if filePath.endswith('.bin') and os.path.exists(filePath):
        return True
    else:
        return False


class MyApp(QtWidgets.QMainWindow, uploader.Ui_MainWindow):
    pathFileFirmware = ''
    pathFileFileSystem = ''

    def __init__(self):
        # Доступ к переменным, метода и т.д. в файле uploader.py
        super().__init__()
        # self.token = None
        self.setupUi(self)  # Инициализация дизайна
        self.UploadButton.clicked.connect(self.upload)  # Связка кнопок и функций-обработчиков
        self.EraseButton.clicked.connect(self.erase)
        self.MakeFirmwareButton.clicked.connect(self.firmware)
        self.MakeFileSystemButton.clicked.connect(self.fileSystem)
        self.ClientSicret.clicked.connect(self.clientSicret)

    # Функционал кнопки ClientSicret
    # Авторизация в Google и добавление данных в таблицу
    def clientSicret(self):
        # self.token, _ = QtWidgets.QFileDialog.getOpenFileName(
        #     self,
        #     'Open File', './',
        #     'Files (*.json)')
        # self.GoogleLine.setText(self.token)
        # creds = Credentials.from_authorized_user_file(self.token, SCOPES)

        creds = None
        if os.path.exists('GoogleAPI/token.json'):
            creds = Credentials.from_authorized_user_file('GoogleAPI/token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'GoogleAPI/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('GoogleAPI/token.json', 'w') as token:
                token.write(creds.to_json())

        self.GoogleLine.setText('GoogleAPI/token.json')
        try:
            service = build('sheets', 'v4', credentials=creds)

            sheet = service.spreadsheets()
            response = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={u'range': 'A1:B', u'values': [[u'id1', u'password1'], [u'id2', u'password2']],
                      u'majorDimension': u'ROWS'}).execute()
        except HttpError as err:
            print(err)

    # Функционал кнопки Upload
    # загрузка прошивки на устройство
    def upload(self):
        portName = str(self.ComPortComboBox.currentText())
        port = serial.Serial(portName)
        baud = str(port.baudrate)  # скорость работы порта

        eraseFlash(port=portName, baud=baud)
        flashFirmware(port=portName, baud=baud)
        flashSPIFFS(port=portName, baud=baud)

        deviceId = getSerialNum(port)
        password = generatePassword(deviceId)
        if deviceId is False:
            self.labelStatus.clear()
            self.labelPassword.clear()
            self.labelStatus.setStyleSheet("background-color: rgb(220,20,60);;\n"
                                           "border-radius:  10px;\n"
                                           "color:  rgb(220,20,60);")
            self.labelPassword.setStyleSheet("background-color: rgb(220,20,60);;\n"
                                             "border-radius:  10px;\n"
                                             "color:  rgb(220,20,60);")
        else:
            self.labelStatus.setText('Successfully: ' + deviceId)
            self.labelPassword.setText('Pass: ' + password)

    # Функционал кнопки Erase
    def erase(self):
        portName = str(self.ComPortComboBox.currentText())
        eraseFlash(port=portName, baud=self.BAUD)

    # Функционал кнопки Firmware
    # Выбор файла с прошивкой
    def firmware(self):
        if checkFile(self.FirmfareLine.text()):  # Если в соответствующем поле введен кореектный путь, используем его
            self.pathFileFirmware = self.FirmfareLine.text()
            self.MakeFileSystemButton.setEnabled(True)
        else:                                    # иначе выбираем файл в проводнике
            self.pathFileFirmware, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                'Open File', './',
                'Files (*.bin)')
            if checkFile(self.pathFileFirmware):
                self.FirmfareLine.setText(self.pathFileFirmware)
                self.MakeFileSystemButton.setEnabled(True)

    # Функционал кнопки FileSystem
    # Выбор файла с файловой системой
    def fileSystem(self):
        if checkFile(self.FileSistemLine.text()):  # Если в соответствующем поле введен кореектный путь, используем его
            self.pathFileFileSystem = self.FileSistemLine.text()
            self.EraseButton.setEnabled(True)
            self.UploadButton.setEnabled(True)
            self.ClientSicret.setEnabled(True)
        else:                                      # иначе выбираем файл в проводнике
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
    window = MyApp()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
