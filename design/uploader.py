import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import serial.tools.list_ports


# Функция для получения списка доступных COM портов
# Возвращаемое значение list(str) - список портов
def getPortList():
    ports = serial.tools.list_ports.comports()
    available = []
    for port, desc, hwid in sorted(ports):
        available.append(port)
    return available


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(680, 400)
        MainWindow.setMinimumSize(QtCore.QSize(680, 400))
        MainWindow.setMaximumSize(QtCore.QSize(680, 400))
        MainWindow.setToolTip("")
        MainWindow.setStyleSheet("background-color:rgb(80, 50, 44);")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.UploadButton.setEnabled(False)
        self.UploadButton.setGeometry(QtCore.QRect(419, 330, 241, 50))
        self.UploadButton.setStyleSheet("QPushButton {\n"
                                        "    background-color: rgb(224, 162, 25);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed {\n"
                                        "    background-color:  rgb(241, 218, 141);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:disabled {\n"
                                        "    background-color:  rgb(192, 192, 192);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}")
        self.UploadButton.setObjectName("UploadButton")
        self.EraseButton = QtWidgets.QPushButton(self.centralwidget)
        self.EraseButton.setEnabled(False)
        self.EraseButton.setGeometry(QtCore.QRect(30, 330, 211, 50))
        self.EraseButton.setStyleSheet("QPushButton {\n"
                                       "    border-radius:  10px;\n"
                                       "    background-color:rgb(220, 82, 140);\n"
                                       "    color:  rgb(255, 255, 255);\n"
                                       "    font-size:  33px;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed {\n"
                                       "    background-color:  rgb(174, 109, 132);\n"
                                       "}\n"
                                       "QPushButton:disabled {\n"
                                       "    background-color:  rgb(192, 192, 192);\n"
                                       "    border-radius:  10px;\n"
                                       "    color:  rgb(255, 255, 255);\n"
                                       "    font-size:  33px;\n"
                                       "}")
        self.EraseButton.setObjectName("EraseButton")
        self.MakeFirmwareButton = QtWidgets.QPushButton(self.centralwidget)
        self.MakeFirmwareButton.setGeometry(QtCore.QRect(450, 30, 210, 50))
        self.MakeFirmwareButton.setStyleSheet("QPushButton {\n"
                                              "    border-radius:  10px;\n"
                                              "    background-color: rgb(224, 162, 25);\n"
                                              "    color:  rgb(255, 255, 255);\n"
                                              "    font-size:  33px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color:  rgb(241, 218, 141);\n"
                                              "}")
        self.MakeFirmwareButton.setObjectName("MakeFirmwareButton")
        self.MakeFileSystemButton = QtWidgets.QPushButton(self.centralwidget)
        self.MakeFileSystemButton.setEnabled(False)
        self.MakeFileSystemButton.setGeometry(QtCore.QRect(450, 100, 210, 50))
        self.MakeFileSystemButton.setStyleSheet("QPushButton {\n"
                                                "    border-radius:  10px;\n"
                                                "    background-color:rgb(180, 50, 185);\n"
                                                "    color:  rgb(255, 255, 255);\n"
                                                "    font-size:  33px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: rgb(181, 86, 185);\n"
                                                "}\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color:  rgb(192, 192, 192);\n"
                                                "    border-radius:  10px;\n"
                                                "    color:  rgb(255, 255, 255);\n"
                                                "    font-size:  33px;\n"
                                                "}")
        self.MakeFileSystemButton.setObjectName("MakeFileSystemButton")
        self.FirmfareLine = QtWidgets.QLineEdit(self.centralwidget)
        self.FirmfareLine.setGeometry(QtCore.QRect(30, 30, 400, 50))
        self.FirmfareLine.setStyleSheet("border-radius:  10px;\n"
                                        " background-color: rgb(188, 210, 221);\n"
                                        "color:  rgb(0, 0, 0);\n"
                                        "font-size:  33px;")
        self.FirmfareLine.setObjectName("FirmfareLine")
        self.FileSistemLine = QtWidgets.QLineEdit(self.centralwidget)
        self.FileSistemLine.setGeometry(QtCore.QRect(30, 100, 400, 50))
        self.FileSistemLine.setStyleSheet("border-radius:  10px;\n"
                                          " background-color: rgb(188, 210, 221);\n"
                                          "color:  rgb(0, 0, 0);\n"
                                          "font-size:  33px;")
        self.FileSistemLine.setObjectName("FileSistemLine")
        self.ComPortComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.ComPortComboBox.setEnabled(True)
        self.ComPortComboBox.setGeometry(QtCore.QRect(270, 330, 121, 50))
        self.ComPortComboBox.setStyleSheet("QComboBox {\n"
                                           "   font-size:  33px;\n"
                                           "    border-radius:  10px;\n"
                                           "    background-color: rgb(188, 210, 221);\n"
                                           "    padding: 1px 18px 1px 3px;\n"
                                           "\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:editable {\n"
                                           "    background: rgb(188, 210, 221);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:!editable, QComboBox::drop-down:editable {\n"
                                           "     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                           "                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
                                           "                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
                                           "}\n"
                                           "\n"
                                           "/* QComboBox gets the \"on\" state when the popup is open */\n"
                                           "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
                                           "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
                                           "                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
                                           "                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:on { /* shift the text when the popup opens */\n"
                                           "    padding-top: 3px;\n"
                                           "    padding-left: 4px;\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox::drop-down {\n"
                                           "    subcontrol-origin: padding;\n"
                                           "    subcontrol-position: top right;\n"
                                           "    width: 15px;\n"
                                           "\n"
                                           "    border-left-width: 1px;\n"
                                           "    border-left-color: darkgray;\n"
                                           "    border-left-style: solid; /* just a single line */\n"
                                           "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                           "    border-bottom-right-radius: 3px;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
                                           "    top: 1px;\n"
                                           "    left: 1px;\n"
                                           "}")
        self.ComPortComboBox.setObjectName("ComPortComboBox")

        self.GoogleLine = QtWidgets.QLineEdit(self.centralwidget)
        self.GoogleLine.setGeometry(QtCore.QRect(30, 180, 371, 50))
        self.GoogleLine.setStyleSheet("border-radius:  10px;\n"
                                      " background-color: rgb(188, 210, 221);\n"
                                      "color:  rgb(0, 0, 0);\n"
                                      "font-size:  33px;")
        self.GoogleLine.setObjectName("GoogleLine")
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setEnabled(True)
        self.labelStatus.setGeometry(QtCore.QRect(30, 250, 371, 50))
        self.labelStatus.setStyleSheet("background-color: rgb(11, 118, 64);;\n"
                                       "border-radius:  10px;\n"
                                       "color:  rgb(255, 255, 255);\n"
                                       "font-size:  33px;")
        self.labelStatus.setObjectName("labelStatus")
        self.labelPassword = QtWidgets.QLabel(self.centralwidget)
        self.labelPassword.setEnabled(True)
        self.labelPassword.setGeometry(QtCore.QRect(420, 250, 241, 50))
        self.labelPassword.setStyleSheet("background-color: rgb(11, 118, 64);;\n"
                                         "border-radius:  10px;\n"
                                         "color:  rgb(255, 255, 255);\n"
                                         "font-size:  33px;")
        self.labelPassword.setObjectName("labelPassword")
        self.ClientSicret = QtWidgets.QPushButton(self.centralwidget)
        self.ClientSicret.setEnabled(False)
        self.ClientSicret.setGeometry(QtCore.QRect(420, 180, 241, 50))
        self.ClientSicret.setStyleSheet("QPushButton {\n"
                                        "    background-color:rgb(16, 167, 96);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed {\n"
                                        "    background-color: rgb(11, 118, 64);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:disabled {\n"
                                        "    background-color:  rgb(192, 192, 192);\n"
                                        "    border-radius:  10px;\n"
                                        "    color:  rgb(255, 255, 255);\n"
                                        "    font-size:  33px;\n"
                                        "}")
        self.ClientSicret.setObjectName("ClientSicret")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.UploadButton.setText(_translate("MainWindow", "Upload"))
        self.EraseButton.setText(_translate("MainWindow", "Erase"))
        self.MakeFirmwareButton.setText(_translate("MainWindow", "Firmware"))
        self.MakeFileSystemButton.setText(_translate("MainWindow", "FileSystem"))

        # Добавляем список доступных COM портов в всплывающий список
        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            self.ComPortComboBox.addItem(info.portName())

        self.labelStatus.setText(_translate("MainWindow", "Successfully:"))
        self.labelPassword.setText(_translate("MainWindow", "Pass:"))
        self.ClientSicret.setText(_translate("MainWindow", "Client Secret"))
