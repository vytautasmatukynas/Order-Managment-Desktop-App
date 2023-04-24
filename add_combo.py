import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from configparser import ConfigParser

import style_gray

import config

params = config.sql_db

# # create a parser
# parser = ConfigParser()
# # read config file
# parser.read('config.ini')
#
# params = {}
# if 'postgreDB' in parser:
#     for key in parser['postgreDB']:
#         params[key] = parser['postgreDB'][key]
# else:
#     raise Exception(
#         'Section {0} not found in the {1} file'.format('postgreDB', 'config.ini'))


class AddCombo(QDialog):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle('ADD ComboBox ITEMS')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 400, 280)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Order App', 'Combo')
        # print(self.settings.fileName())
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

        self.UI()
        self.show()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        # uzsakymai ########################
        self.companyE = QLineEdit()
        self.companyE.setFont(QFont("Times", 12))

        self.clientE = QLineEdit()
        self.clientE.setFont(QFont("Times", 12))

        self.phoneE = QLineEdit()
        self.phoneE.setFont(QFont("Times", 12))

        self.nameE = QLineEdit()
        self.nameE.setFont(QFont("Times", 12))

        self.okBtn = QPushButton("UPDATE")
        self.okBtn.clicked.connect(self.addCombo)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)

        self.cancelBtn = QPushButton("CLOSE")
        self.cancelBtn.clicked.connect(self.closeAddCombo)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QGridLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QGroupBox("Order Combo Items:")
        self.widgetFrame.setFont(QFont("Times", 12))

        ############################## UZSAKYMAI
        self.widgetLayout.addRow(QLabel("Company: "), self.companyE)
        self.widgetLayout.addRow(QLabel("Client: "), self.clientE)
        self.widgetLayout.addRow(QLabel("Phone Number: "), self.phoneE)
        self.widgetLayout.addRow(QLabel("Order Name: "), self.nameE)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetFrame.setLayout(self.widgetLayout)

        ####################################
        self.mainLayout.addWidget(self.widgetFrame, 0, 0)
        self.mainLayout.addWidget(self.okBtn, 1, 0)
        self.mainLayout.addWidget(self.cancelBtn, 2, 0)

        #################################
        self.setLayout(self.mainLayout)

    def addCombo(self):
        company = self.companyE.text().upper()
        client = self.clientE.text().upper()
        phone = self.phoneE.text().upper()
        name = self.nameE.text()

        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute('''INSERT INTO combo_orders (uzsakymai_company, uzsakymai_client, uzsakymai_phone, 
                        uzsakymai_name) VALUES (%s, %s, %s, %s)''',
                      (company, client, phone, name))

            con.commit()

            con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        finally:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Has been successfully added.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def closeAddCombo(self):
        self.close()
