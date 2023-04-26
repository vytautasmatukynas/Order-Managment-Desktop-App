import ctypes
from pathlib import Path

import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
import style_gray

params = config.sql_db

# create a parser
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

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()

# get windows scale ratio
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

scale_factor = user32.GetDpiForSystem() / 96.0
# print("Scale factor:", scale_factor)

# change widget size to scale ratio
TEXT_PT = int(12 * scale_factor)
BUTTON_HEIGHT = int(25 * scale_factor)
ENTRY_COMBO_HEIGHT = int(25 * scale_factor)


class Addorders(QDialog):
    """add new record class"""

    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / scale_factor), int(300 / scale_factor),
                         int(1000 * scale_factor), int(432 * scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.UI()

        self.show()

        style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Order App', 'Add1')
        # print(self.settings.fileName())
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

    def closeEvent(self, event):
        self.settings.setValue('scale_aware', True)
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        conn = psycopg2.connect(
            **params
        )
        cur = conn.cursor()
        cur.execute("""SELECT * FROM combo_orders ORDER BY id ASC""")
        query = cur.fetchall()

        list_company_start = [item[1] for item in query]
        list_company = []
        for a in list_company_start:
            list_company.append(a)
            if a == None or a == "":
                list_company.remove(a)

        list_client_start = [item[2] for item in query]
        list_client = []
        for b in list_client_start:
            list_client.append(b)
            if b == None or b == "":
                list_client.remove(b)

        list_phone_start = [item[3] for item in query]
        list_phone = []
        for c in list_phone_start:
            list_phone.append(c)
            if c == None or c == "":
                list_phone.remove(c)

        list_name_start = [item[4] for item in query]
        list_name = []
        for d in list_name_start:
            list_name.append(d)
            if d == None or d == "":
                list_name.remove(d)

        conn.close()

        self.companyCombo = QComboBox()
        self.companyCombo.setEditable(True)
        self.companyCombo.setPlaceholderText('Text')
        self.companyCombo.addItems(list_company)
        self.companyCombo.setFont(QFont("Times", 12))

        self.clientCombo = QComboBox()
        self.clientCombo.setEditable(True)
        self.clientCombo.setPlaceholderText('Text')
        self.clientCombo.addItems(list_client)
        self.clientCombo.setFont(QFont("Times", 12))

        self.phoneCombo = QComboBox()
        self.phoneCombo.setEditable(True)
        self.phoneCombo.setPlaceholderText('Text')
        self.phoneCombo.addItems(list_phone)
        self.phoneCombo.setFont(QFont("Times", 12))

        self.nameCombo = QComboBox()
        self.nameCombo.setEditable(True)
        self.nameCombo.setPlaceholderText('Text')
        self.nameCombo.addItems(list_name)
        self.nameCombo.setFont(QFont("Times", 12))

        self.termEntry = QComboBox()
        self.termEntry.setEditable(True)
        self.termEntry.addItems(
            ["-", "+"])
        self.termEntry.setFont(QFont("Times", 12))

        self.statusEntry = QComboBox()
        self.statusEntry.setEditable(True)
        self.statusEntry.setPlaceholderText('Text')
        self.statusEntry.addItems(
            ["FINISHED", "IN PROCESS"])
        self.statusEntry.setFont(QFont("Times", 12))

        self.commentsEntry = QTextEdit()
        self.commentsEntry.setFont(QFont("Times", 12))
        self.commentsEntry.setPlaceholderText('Text')

        self.locEntry = QLineEdit()
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                    "color:black;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.folderBtn = QPushButton("ADD LINK TO FOLDER")
        self.folderBtn.setFixedHeight(BUTTON_HEIGHT)
        self.folderBtn.clicked.connect(self.OpenFolderDialog)
        self.folderBtn.setFont(QFont("Times", 10))

        self.ListEntry = QLineEdit()
        self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")

        self.ListEntry.setFont(QFont("Times", 12))

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.setFixedHeight(BUTTON_HEIGHT)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("ADD DATE")
        self.dateBtn.setFixedWidth(int(110 * scale_factor))
        self.dateBtn.setFixedHeight(BUTTON_HEIGHT)
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFont(QFont("Times", 10))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(BUTTON_HEIGHT)
        self.okBtn.clicked.connect(self.addorders)
        self.okBtn.setFont(QFont("Times", 10))
        # self.okBtn.setMaximumWidth(200)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(BUTTON_HEIGHT)
        self.cancelBtn.clicked.connect(self.cancelordersAdd)
        self.cancelBtn.setFont(QFont("Times", 10))
        # self.cancelBtn.setMaximumWidth(200)

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.topmainLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QVBoxLayout()
        self.mainLayout2 = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()
        self.widgetFrame.setFont(QFont("Times", 12))
        self.widgetFrame2.setFont(QFont("Times", 12))

        # self.qhbox1 = QHBoxLayout()
        # self.qhbox1.addWidget(self.locEntry)
        # self.qhbox1.addWidget(self.breziniaiBtn)

        # self.qhbox2 = QHBoxLayout()
        # self.qhbox2.addWidget(self.ListEntry)
        # self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.termEntry)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("Company:"), self.companyCombo)
        self.widgetLayout.addRow(QLabel("Client:"), self.clientCombo)
        self.widgetLayout.addRow(QLabel("Phone Number:"), self.phoneCombo)
        self.widgetLayout.addRow(QLabel("Order Name:"), self.nameCombo)
        self.widgetLayout.addRow(QLabel("Order Term:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("Order Status:"), self.statusEntry)

        self.widgetLayout.addRow(QLabel("Add Folder:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.folderBtn)
        self.widgetLayout.addRow(QLabel("Add File:"), self.ListEntry)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("Comments:"))
        self.widgetLayout2.addRow(self.commentsEntry)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        # """add widgets to layouts"""
        self.mainLayout1.addWidget(self.widgetFrame)
        self.mainLayout2.addWidget(self.widgetFrame2)

        self.mainLayout.addLayout(self.mainLayout1, 37)
        self.mainLayout.addLayout(self.mainLayout2, 63)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        """get folder dir"""
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def convertToBinaryDataFile(self, filename):
        # Convert digital data to binary format
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        except:
            pass

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.pdf;*.txt;*.jpg;*.png)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name

        justfilename = getfullfilename[:-4]
        filetype = getfullfilename[-4:]

        # print(directory)
        # print(justfilename)
        # print(filetype)

        self.ListDir.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetype))

        self.ListEntry.setText(f"{justfilename}{filetype}")

    def terminasCalendar(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(BUTTON_HEIGHT)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QDialog()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(int(780 / scale_factor), int(280 / scale_factor),
                                        int(350 * scale_factor), int(350 * scale_factor))
        self.calendarWindow.setWindowTitle('TERMINAS')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        style_gray.QCalendarstyle(self)
        self.calendarWindow.show()

        # @QtCore.pyqtSlot(QtCore.QDate)
        def get_date(qDate):
            if qDate.day() <= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            elif qDate.day() <= 9 and qDate.month() >= 10:
                date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            elif qDate.day() >= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            else:
                date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            self.calendarWindow.close()

        self.cal.clicked.connect(get_date)

    def cal_cancel(self):
        self.calendarWindow.close()

    def addorders(self):
        company = self.companyCombo.currentText().upper()
        client = self.clientCombo.currentText().upper()
        phone = self.phoneCombo.currentText().upper()
        name = self.nameCombo.currentText()
        term = self.termEntry.currentText()
        status = self.statusEntry.currentText().upper()
        comments = str(self.commentsEntry.toPlainText())
        folder = self.locEntry.text()
        file = self.ListEntry.text()
        update_date1 = self.update_date.text()

        filename = self.ListFileName.text()
        byteaPhoto = self.convertToBinaryDataFile(self.ListDir.text())
        listfiletype = self.ListFileType.text()
        listentry = self.ListDir.text()

        terminas_date = ""

        if term != terminas_date:
            # try:
            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()

            cur.execute('''INSERT INTO orders (company, client, phone_number, order_name,
                order_term, status, comments, order_folder, order_file, update_date,
                filename, photo, filetype, filedir) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (company, client, phone, name,
                         term, status, comments, folder, file, update_date1,
                         filename, byteaPhoto, listfiletype, listentry))

            conn.commit()

            conn.close()

            # except (Exception, psycopg2.Error) as error:
            #     print("Error while fetching data from PostgreSQL", error)
            #     msg = QMessageBox()
            #     msg.setWindowTitle("ERROR...")
            #     msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            #     msg.setIcon(QMessageBox.Warning)
            #     msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
            #
            #     style_gray.msgsheetstyle(msg)
            #
            #     x = msg.exec_()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("TERMINAS can't be empty...")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelordersAdd(self):
        self.close()


def main():
    import sys

    App = QApplication(sys.argv)

    window = Addorders()

    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
