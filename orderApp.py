import os
import shutil
import sys
import webbrowser
from pathlib import Path

import psycopg2
import requests
import xlwt
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from configparser import ConfigParser

import add_combo
import add_order
import style_gray

# create a parser
parser = ConfigParser()
# read config file
parser.read('config.ini')

params = {}
if 'postgreDB' in parser:
    for key in parser['postgreDB']:
        params[key] = parser['postgreDB'][key]
else:
    raise Exception(
        'Section {0} not found in the {1} file'.format('postgreDB', 'config.ini'))

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()

__author__ = 'Vytautas Matukynas'
__copyright__ = f'Copyright (C) {year}, Vytautas Matukynas'
__credits__ = ['Vytautas Matukynas']
__license__ = 'Vytautas Matukynas'
__version__ = '1.00'
__maintainer__ = 'Vytautas Matukynas'
__email__ = 'vytautas.matukynas@gmail.com'
__status__ = 'Beta'
_AppName_ = 'Order App'


# align for QTable class, DELEGATE ALIGNMENT
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        """Delegate style to items"""
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class MainMenu(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        # mainWindow
        self.setWindowTitle("Order App")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(100, 100, 1200, 720)
        self.showMaximized()

        # MainClass functions
        self.show()
        self.UI()

    def UI(self):
        """Function that starts at start"""
        style_gray.SheetStyle(self)
        self.menubar()
        self.searchWidgets()
        self.treeTableItems()
        self.toolBarInside()
        self.tableWidgets()
        self.timeWidget()
        self.layouts()
        self.updateInfoOnStart()

    def menubar(self):
        """Menu bar"""
        self.menuBarMain = self.menuBar()
        self.menuBarMain.isRightToLeft()

        # File bar
        file = self.menuBarMain.addMenu("File")
        # Submenu bar
        new = QAction("New", self)
        new.triggered.connect(self.add_orders)
        new.setShortcut("Ctrl+N")
        file.addAction(new)

        file.addSeparator()
        save = QAction("save", self)
        save.triggered.connect(self.save)
        save.setShortcut("Ctrl+S")
        save.setIcon(QIcon("icons/save.png"))
        file.addAction(save)
        saveAs = QAction("Save As", self)
        saveAs.triggered.connect(self.saveAs)
        saveAs.setShortcut("Alt+S")
        saveAs.setIcon(QIcon("icons/saveas.png"))
        file.addAction(saveAs)
        file.addSeparator()
        delete = QAction("Delete", self)
        delete.triggered.connect(self.deleteItem)
        delete.setIcon(QIcon("icons/delete.png"))
        file.addAction(delete)
        file.addSeparator()
        refresh = QAction("Refresh", self)
        refresh.triggered.connect(self.listTables)
        refresh.setShortcut("F5")
        refresh.setIcon(QIcon("icons/refresh.png"))
        file.addAction(refresh)
        file.addSeparator()
        print = QAction("Print", self)
        print.triggered.connect(self.handlePreview)
        print.setShortcut("Ctrl+P")
        print.setIcon(QIcon("icons/print.png"))
        file.addAction(print)
        file.addSeparator()
        exit = QAction("Exit", self)
        exit.triggered.connect(self.MainClose)
        exit.setShortcut("Ctrl+Q")
        exit.setIcon(QIcon("icons/exit.png"))
        file.addAction(exit)

        # Setting bar
        Settings = self.menuBarMain.addMenu("Settings")

        Style = Settings.addMenu("Style")
        Style.setIcon(QIcon("icons/design.png"))

        Group = QActionGroup(Style)

        style2 = QAction("Gandalf the Grey", self)
        style2.setCheckable(True)
        style2.setChecked(True)
        Style.addAction(style2)

        # Group.addAction(style1)
        Group.addAction(style2)

        # Check only one item in GroupBox
        Group.setExclusive(True)

        Settings.addSeparator()

        combo_box = QAction("Edit ComboBox", self)
        combo_box.triggered.connect(self.add_combo)
        Settings.addAction(combo_box)

        # Help bar
        help = self.menuBarMain.addMenu("Help")

        # Submenu bar
        UpdateApp = QAction("Check for Updates", self)
        UpdateApp.setIcon(QIcon("icons/update.png"))
        UpdateApp.triggered.connect(self.updateInfo)
        help.addAction(UpdateApp)
        help.addSeparator()
        Info = QAction("About", self)
        Info.setIcon(QIcon("icons/info.png"))
        Info.triggered.connect(self.helpinfo)
        help.addAction(Info)

    def updateInfoOnStart(self):
        """version check"""
        try:
            # Version file link
            response = requests.get(
                'https://gist.githubusercontent.com/xxxxxx')
            data = response.text

            if float(data) > float(__version__):
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                style_gray.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    # Donwload file link
                    webbrowser.open_new_tab(
                        'https://drive.google.com/file/xxxxxxx')

                    self.MainClose()

                else:
                    pass

            else:
                pass

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def updateInfo(self):
        try:
            response = requests.get(
                'https://gist.githubusercontent.com/xxxxxxx')
            data = response.text

            if float(data) > float(__version__):
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                style_gray.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    webbrowser.open_new_tab(
                        'https://drive.google.com/file/xxxxxxxx')

                    self.MainClose()

                else:
                    pass

            else:
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('No updates, version {}.'.format(__version__))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                style_gray.msgsheetstyle(msg)

                x = msg.exec_()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def helpinfo(self):
        # QMessageBox.information(self, "ABOUT", "If you want to find a needle in a haystack,\n"
        #                                        "burn the haystack.")
        msg = QMessageBox()
        msg.setWindowTitle("ABOUT")
        msg.setText("If you want to find a needle in a haystack,\n"
                    "burn the haystack.\n"
                    "\n"
                    "Order App version {} ({})\n"
                    "\n"
                    "{}".format(__version__, __status__, __copyright__))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

        style_gray.msgsheetstyle(msg)

        x = msg.exec_()

    def tableWidgets(self):
        """Tables"""
        # UZSAKYMAI TABLE
        self.emptyTable = QTableWidget()
        self.emptyTable.setColumnCount(0)

        self.ordersTable = QTableWidget()
        self.ordersTable.setColumnCount(11)
        self.ordersTable.setColumnHidden(0, True)
        self.ordersTable.setColumnHidden(8, True)
        # self.uzsakymuTable.setColumnHidden(9, True)
        self.ordersTable.setSortingEnabled(True)

        # for number in [1, 2, 3, 4, 5, 6, 9, 10]:
        #     self.uzsakymuTable.setColumnWidth(number, 150)

        headers_uzsk = ["ID", "COMPANY", "CLIENT", "PHONE NUMBER", "ORDER NAME", "ORDER TERM",
                        "STATUS", "COMMENTS", "FOLDER LINK", "ORDER FILE", "UPDATED"]

        for column_number in range(0, len(headers_uzsk)):
            while column_number < len(headers_uzsk):
                header_name = headers_uzsk[column_number]
                self.ordersTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.ordersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.horizontalHeader().setHighlightSections(False)
        self.ordersTable.horizontalHeader().setDisabled(True)
        self.ordersTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.ordersTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.ordersTable.clicked.connect(self.uzsakymai_select)
        self.ordersTable.doubleClicked.connect(self.updateorders)

        # Align delegate Class
        delegate = AlignDelegate()

        # for column
        for number in [1, 2, 3, 4, 5, 6, 9, 10]:
            self.ordersTable.setItemDelegateForColumn(number, delegate)

        # for all columns
        # self.uzsakymuTable.setItemDelegate(delegate)
        # self.atsarguTable.setItemDelegate(delegate)
        # self.sanaudosTable.setItemDelegate(delegate)
        # self.stelazasTable.setItemDelegate(delegate)
        # self.rolikaiTable.setItemDelegate(delegate)

    def searchWidgets(self):
        self.cancelButton1 = QPushButton("CANCEL")
        self.cancelButton1.setFixedHeight(25)
        self.cancelButton1.setFixedWidth(90)
        self.cancelButton1.clicked.connect(self.clearSearchEntry)
        self.cancelButton1.setFont(QFont("Times", 10))

        self.searchButton1 = QPushButton("SEARCH")
        self.searchButton1.setFixedHeight(25)
        self.searchButton1.setFixedWidth(90)
        self.searchButton1.clicked.connect(self.searchTables)
        self.searchButton1.setFont(QFont("Times", 10))

        self.searchEntry1 = QLineEdit()
        self.searchEntry1.setFixedHeight(25)
        self.searchEntry1.setPlaceholderText('Filter table...')

        self.cancelButton2 = QPushButton("CANCEL")
        self.cancelButton2.setFixedHeight(25)
        self.cancelButton2.setFixedWidth(90)
        self.cancelButton2.clicked.connect(self.clearSearchEntry2)
        self.cancelButton2.setFont(QFont("Times", 10))

        self.searchEntry2 = QLineEdit()
        self.searchEntry2.setFixedHeight(25)
        self.searchEntry2.setPlaceholderText('Select table items...')
        self.searchEntry2.textChanged.connect(self.searchTables2)

    def treeTableItems(self):
        """Treeview table"""
        self.treeTable = QTreeWidget()
        self.treeTable.setAnimated(True)
        self.treeTable.setHeaderHidden(True)
        self.treeTable.setColumnCount(1)
        self.treeTable.setFixedWidth(150)

        self.ordersSelect = QTreeWidgetItem(self.treeTable, ["Orders"])
        self.ordersSelect.setExpanded(True)

        self.ordersSelect1 = ["Finished", "In Process"]
        for item1 in self.ordersSelect1:
            self.ordersSelect.addChild(QTreeWidgetItem([item1]))

        self.treeTable.clicked.connect(self.listTables)

    def toolBarInside(self):
        """Toolbar inside table"""
        self.tb2 = QtWidgets.QToolBar("Action tb")
        # self.addToolBar(QtCore.Qt.BottomToolBarArea, self.tb2)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        # self.tb2.setMovable(False)
        self.tb2.setIconSize(QtCore.QSize(17, 17))

        self.add_tb = QAction(QIcon("icons/add.png"), "../add", self)
        self.tb2.addAction(self.add_tb)
        self.add_tb.triggered.connect(self.add_orders)

        self.delete_tb = QAction(QIcon("icons/delete.png"), "Delete", self)
        self.tb2.addAction(self.delete_tb)
        self.delete_tb.triggered.connect(self.deleteItem)

        self.tb2.addSeparator()

        self.refresh_tb = QAction(QIcon("icons/refresh.png"), "Refresh", self)
        self.tb2.addAction(self.refresh_tb)
        self.refresh_tb.triggered.connect(self.listTables)

        self.tb2.addSeparator()

        self.save_tb = QAction(QIcon("icons/save.png"), "../save", self)
        self.tb2.addAction(self.save_tb)
        self.save_tb.triggered.connect(self.save)

        self.saveAs_tb = QAction(QIcon("icons/saveas.png"), "Save As...", self)
        self.tb2.addAction(self.saveAs_tb)
        self.saveAs_tb.triggered.connect(self.saveAs)

    def timeWidget(self):
        # Timer
        self.Timer = QLabel()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)  # update every second

        self.showTime()

    def showTime(self):
        self.currentTime = QTime.currentTime()
        self.displayTxt = self.currentTime.toString('hh:mm:ss')
        self.Timer.setText(self.displayTxt)

    def layouts(self):
        """App layouts"""
        self.mainLayout = QVBoxLayout()

        self.searchLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.LeftLayoutTop = QVBoxLayout()
        self.treeLeftLayout = QVBoxLayout()

        self.searchLayout_table = QHBoxLayout()
        self.tbLayout_table = QHBoxLayout()
        self.tableRightLayout = QStackedLayout()

        self.mainRightLayout = QVBoxLayout()

        # Search layout
        self.searchLayout.addWidget(self.cancelButton1)
        self.searchLayout.addWidget(self.searchButton1)
        self.searchLayout.addWidget(self.searchEntry1)

        # Middle layout
        # Left side
        self.LeftLayoutTop.addWidget(self.treeTable)
        self.treeLeftLayout.addLayout(self.LeftLayoutTop)

        # Right side search
        self.searchLayout_table.addWidget(self.cancelButton2)
        self.searchLayout_table.addWidget(self.searchEntry2)

        # Right side tb
        self.tbLayout_table.addWidget(self.tb2)

        # Right side tables
        self.tableRightLayout.addWidget(self.ordersTable)
        self.tableRightLayout.addWidget(self.emptyTable)
        self.tableRightLayout.setCurrentIndex(1)

        # Right layout with search
        self.mainRightLayout.addLayout(self.searchLayout_table, 1)
        self.mainRightLayout.addLayout(self.tbLayout_table, 1)
        self.mainRightLayout.addLayout(self.tableRightLayout, 97)

        # Bottom layout
        self.bottomLayout.addWidget(QLabel(f"Order App {__version__} ({__status__})"), 98, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(QLabel(f"Current date/time: {datetime.toPyDate()}"), 1, alignment=Qt.AlignRight)
        self.bottomLayout.addWidget(self.Timer, 1, alignment=Qt.AlignRight)

        # Main layout
        self.middleLayout.addLayout(self.treeLeftLayout)
        self.middleLayout.addLayout(self.mainRightLayout)

        self.mainLayout.addLayout(self.searchLayout, 1)
        self.mainLayout.addLayout(self.middleLayout, 98)
        self.mainLayout.addLayout(self.bottomLayout, 1)

        # Central_widget to view widgets
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.central_widget)

    def uzsakymai_select(self):
        global ordersId

        self.listorders = []
        self.num = 0
        self.listorders.append(self.ordersTable.item(self.ordersTable.currentRow(), self.num).text())

        ordersId = self.listorders[0]

    def contextMenuEvent(self, event):
        """Right mouse button select"""
        if self.ordersTable.underMouse():
            global ordersId

            # Left mouse button table
            contextMenu = QMenu(self)

            openFolder = contextMenu.addAction("Open Folder")
            openFolder.triggered.connect(self.openFolder)
            openFolder.setShortcut("Alt+D")
            openFolder.setIcon(QIcon("icons/drawings.png"))
            contextMenu.addSeparator()
            openFile = contextMenu.addAction("Open File")
            openFile.triggered.connect(self.openFile)
            openFile.setShortcut("Alt+L")
            openFile.setIcon(QIcon("icons/files.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_orders)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.listTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            delete = contextMenu.addAction("Delete")
            delete.triggered.connect(self.deleteItem)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def listTables(self):
        """sort"""
        # Get current date
        if datetime.day() <= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-0{2}".format(year, month, day))
        elif datetime.day() <= 9 and datetime.month() >= 10:
            date = ("{0}-{1}-0{2}".format(year, month, day))
        elif datetime.day() >= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-{2}".format(year, month, day))
        else:
            date = ("{0}-{1}-{2}".format(year, month, day))

        try:
            if self.treeTable.currentItem() == self.ordersSelect:
                self.tableRightLayout.setCurrentIndex(0)
                # Cleans table
                self.ordersTable.setFont(QFont("Times", 10))

                for i in reversed(range(self.ordersTable.rowCount())):
                    self.ordersTable.removeRow(i)

                # Connect to SQL table
                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT id, company, client, phone_number, order_name,
                    order_term, status, comments, order_folder, order_file, update_date,
                    filename, filetype, filedir FROM orders 
                    ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
                query = cur.fetchall()

                # Sort table values and adds to table, change color of some values
                for row_date in query:
                    row_number = self.ordersTable.rowCount()
                    self.ordersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        # print(row_number, column_number, data)

                        # check current date and table entry, if nor equal or bigger make it red
                        listdata = []
                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()
                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # list of names and list of colours to name
                        list_names = ['FINISHED', 'IN PROCESS']
                        list_colors = [(0, 204, 0, 110), (240, 248, 255)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        self.ordersTable.setItem(row_number, column_number, setitem)

                # Edit column cell disable
                self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.ordersSelect.child(0):
                self.tableRightLayout.setCurrentIndex(0)
                self.ordersTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.ordersTable.rowCount())):
                    self.ordersTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT id, company, client, phone_number, order_name,
                    order_term, status, comments, order_folder, order_file, update_date,
                    filename, filetype, filedir FROM orders
                    WHERE statusas = 'FINISHED' 
                    ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.ordersTable.rowCount()
                    self.ordersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))
                        # check current date and table entry, if nor equal or more make it red
                        listdata = []
                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()
                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # list of names and list of colours to name
                        list_names = ['FINISHED', 'IN PROCESS']
                        list_colors = [(0, 204, 0, 110), (240, 248, 255)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        self.ordersTable.setItem(row_number, column_number, setitem)

                self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            elif self.treeTable.currentItem() == self.ordersSelect.child(1):
                self.tableRightLayout.setCurrentIndex(0)
                self.ordersTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.ordersTable.rowCount())):
                    self.ordersTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT id, company, client, phone_number, order_name,
                    order_term, status, comments, order_folder, order_file, update_date,
                    filename, filetype, filedir FROM orders 
                    WHERE statusas = 'IN PROCESS' 
                    ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.ordersTable.rowCount()
                    self.ordersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))
                        # check current date and table entry, if nor equal or more make it red
                        listdata = []
                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()
                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # list of names and list of colours to name
                        list_names = ['FINISHED', 'IN PROCESS']
                        list_colors = [(0, 204, 0, 110), (240, 248, 255)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        self.ordersTable.setItem(row_number, column_number, setitem)

                self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def add_combo(self):
        self.edit_combobox = add_combo.AddCombo()
        self.edit_combobox.exec_()

    def add_orders(self):
        try:
            self.neworders = add_order.Addorders()
            # Refresh table after executing QDialog .exec_
            self.neworders.exec_()
            self.listTables()
        except:
            pass

    def updateorders(self):
        """select row data and fill entry with current data"""
        global ordersId

        try:
            self.display = orderUpdate()
            self.display.show()
            self.display.exec_()
            self.listTables()

        except:
            pass

    def searchTables(self):
        """SEARCH FROM SQL TABLE AND REFRESH QTABLE TO VIEW JUST SEARCHED ITEMS"""
        # Get current date
        if datetime.day() <= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-0{2}".format(year, month, day))
        elif datetime.day() <= 9 and datetime.month() >= 10:
            date = ("{0}-{1}-0{2}".format(year, month, day))
        elif datetime.day() >= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-{2}".format(year, month, day))
        else:
            date = ("{0}-{1}-{2}".format(year, month, day))

        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                a = a1 = a2 = a3 = a4 = self.searchEntry1.text()

                self.ordersTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.ordersTable.rowCount())):
                    self.ordersTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM orders WHERE company ILIKE '%{}%' OR client ILIKE '%{}%' OR 
                    order_name ILIKE '%{}%' OR phone_number ILIKE '%{}%' OR comments ILIKE '%{}%'""".format
                    (a, a1, a2, a3, a4))
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.ordersTable.rowCount()
                    self.ordersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        # print(row_number, column_number, data)

                        # check current date and table entry, if nor equal or bigger make it red
                        listdata = []
                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()
                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                            # list of names and list of colours to name
                            list_names = ['FINISHED', 'IN PROCESS']
                            list_colors = [(0, 204, 0, 110), (255, 255, 255)]
                            for count_num in range(0, len(list_names)):
                                while count_num < len(list_names):
                                    if data == list_names[count_num]:
                                        setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                    count_num += 1

                        self.ordersTable.setItem(row_number, column_number, setitem)

                self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def clearSearchEntry(self):
        """search cancel"""
        self.searchEntry1.clear()
        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                self.listTables()

        except:
            pass

    def searchTables2(self, s):
        """search for items and select matched items"""
        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                # Clear current selection
                self.ordersTable.setCurrentItem(None)

                if not s:
                    # Empty string, do not search
                    return

                matching_items = self.ordersTable.findItems(s, Qt.MatchContains)
                if matching_items:
                    # if it finds something
                    for item in matching_items:
                        item.setSelected(True)
                        item.setSelected(True)

        except:
            pass

    def clearSearchEntry2(self):
        """search cancel"""
        self.searchEntry2.clear()

    def deleteItem(self):
        """deletes item and refresh list"""
        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):

                global ordersId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )

                        cur = conn.cursor()
                        cur.execute("DELETE FROM orders WHERE id = %s", (ordersId,))
                        conn.commit()
                        conn.close()

                        self.listTables()

                    elif (x == QMessageBox.No):
                        pass

                except (Exception, psycopg2.Error) as error:
                    print("Error while fetching data from PostgreSQL", error)
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR...")
                    msg.setText(f"Please first select ROW you want to delete.")
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                    style_gray.msgsheetstyle(msg)

                    x = msg.exec_()

        except:
            pass

    def save(self):
        try:
            self.table_name = ""

            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                self.table_name = "orders"

            query = """SELECT * FROM {}""".format(self.table_name)

            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()

            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

            with open('{}'.format(self.table_name), 'wb') as f:
                cur.copy_expert(outputquery, f)

            conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        finally:
            path = "../save"
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

            src_path = r'{}'.format(table_name)
            dst_path = r'save\{}_{}'.format(table_name, datetime.toPyDate())
            shutil.move(src_path, dst_path)

    def saveAs(self):
        """save table to .xls .csv"""
        try:
            model = ""

            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                model = self.ordersTable.model()
                table = self.ordersTable
                self.table_name = orders

            filename, file_end = QFileDialog.getSaveFileName(self, 'Save', '',
                                                             ".xls(*.xls);; .csv(*.csv);; .pdf(*.pdf)")

            if not filename:
                return

            if file_end == ".xls(*.xls)":
                wbk = xlwt.Workbook()
                sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
                style = xlwt.XFStyle()
                font = xlwt.Font()
                font.bold = True
                style.font = font

                # set borders for the style
                borders = xlwt.Borders()
                borders.left = xlwt.Borders.THIN
                borders.right = xlwt.Borders.THIN
                borders.top = xlwt.Borders.THIN
                borders.bottom = xlwt.Borders.THIN
                style.borders = borders

                # iterate over visible columns only
                visible_cols = [c for c in range(model.columnCount()) if table.isColumnHidden(c) == False]
                for i, c in enumerate(visible_cols):
                    header_text = model.headerData(c, QtCore.Qt.Horizontal)
                    sheet.write(0, i, header_text, style=style)

                    col_width = len(str(header_text))  # initialize column width to the length of the header text
                    for r in range(model.rowCount()):
                        text = str(model.data(model.index(r, c)))
                        col_width = max(col_width, len(text))  # update column width based on the length of the text
                        sheet.write(r + 1, i, text)  # write cell data to the Excel sheet

                    # if the column width is less than the header width, set the column width to the header width
                    if sheet.col(i).width < 256 * (col_width + 1):
                        sheet.col(i).width = 256 * (col_width + 1)

                wbk.save(filename)

            elif file_end == ".csv(*.csv)":
                query = """SELECT * FROM {}""".format(self.table_name)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

                with open('{}'.format(self.table_name), 'wb') as f:
                    cur.copy_expert(outputquery, f)

                conn.close()

            elif file_end == ".pdf(*.pdf)":
                printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
                printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
                printer.setPaperSize(QtPrintSupport.QPrinter.A4)
                printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
                printer.setOutputFileName(filename)

                doc = QtGui.QTextDocument()

                html = """<html>
                <head>
                <style>
                table, th, td {
                  border: 1px solid black;
                  border-collapse: collapse;
                }
                </style>
                </head>"""
                html += "<table><thead>"
                html += "<tr>"
                for c in range(model.columnCount()):
                    if not table.isColumnHidden(c):
                        html += "<th>{}</th>".format(model.headerData(c, QtCore.Qt.Horizontal))

                html += "</tr></thead>"
                html += "<tbody>"
                for r in range(model.rowCount()):
                    html += "<tr>"
                    for c in range(model.columnCount()):
                        if not table.isColumnHidden(c):
                            html += "<td>{}</td>".format(model.index(r, c).data() or "")
                    html += "</tr>"
                html += "</tbody></table>"
                doc.setHtml(html)
                doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))
                doc.print_(printer)

        except:
            pass

    def handlePrint(self):
        """send info to print and prints"""
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        """print preview"""
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        """paint print table"""

        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(0.5)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0)
        tableFormat.setTopMargin(0)
        tableFormat.setCellPadding(4)
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)

        if self.treeTable.currentItem() == self.ordersSelect or \
                self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                self.treeTable.currentItem() == self.ordersSelect.child(1):

            table_name = self.ordersTable

        visible_columns = [col for col in range(table_name.columnCount())
                           if not table_name.isColumnHidden(col)]

        # Get the number of visible columns
        num_visible_cols = len(visible_columns)

        # Insert a table with the number of visible columns and header rows
        table = cursor.insertTable(table_name.rowCount() + 1, num_visible_cols, tableFormat)

        # Set the background color of the header row to light gray and make it bold
        header_format = table.cellAt(0, 0).format()
        header_format.setBackground(QtGui.QColor(230, 230, 230))
        header_cursor = table.cellAt(0, 0).firstCursorPosition()
        header_cursor.insertText("")
        header_format.setFontWeight(QtGui.QFont.Bold)

        for col_index, col in enumerate(visible_columns):
            # Insert header text
            header_cursor = table.cellAt(0, col_index).firstCursorPosition()
            header_cursor.insertText(table_name.horizontalHeaderItem(col).text())
            header_format.setFontWeight(QtGui.QFont.Bold)
            header_format.setBackground(QtGui.QColor(230, 230, 230))
            # Insert data text
            for row in range(1, table.rows()):
                cursor = table.cellAt(row, col_index).firstCursorPosition()
                cursor.insertText(table_name.item(row - 1, col).text())

        # Set the border of the table
        frame_format = table.format()
        frame_format.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
        frame_format.setBorder(0.5)
        frame_format.setBorderBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        document.print_(printer)

    def openFolder(self):
        """open selected folder"""
        try:
            global ordersId

            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()
            cur.execute("""SELECT * FROM orders WHERE ID=%s""", (ordersId,))
            uzsakymas = cur.fetchone()

            uzsakymasFolder = uzsakymas[8]

            conn.close()

            isExist = os.path.exists(uzsakymasFolder)

            if isExist:
                webbrowser.open(os.path.realpath(uzsakymasFolder))

            else:
                if not isExist:
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR...")
                    msg.setText("NO FOLDER...")
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                    style_gray.msgsheetstyle(msg)

                    x = msg.exec_()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to open.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def ordersWriteToFile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def openFile(self):
        """open selected file"""
        global ordersId
        # try:
        con = psycopg2.connect(
            **params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM orders WHERE ID = %s""", (ordersId,))
        uzsakymai = c.fetchone()

        self.filename = uzsakymai[11]
        self.photo = uzsakymai[12]
        self.filetype = uzsakymai[13]

        str_none = ""

        if self.filetype == None or self.filetype == str_none \
                or self.photo == None or self.photo == str_none \
                or self.filename == None or self.filename == str_none:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("NO FILE...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        else:
            path = "uzsakymai_list"
            # Check whether the specified path exists or not
            if not os.path.isdir(path):
                os.makedirs(path)

            photoPath = "uzsakymai_list/" + self.filename + self.filetype

            if not os.path.isfile(photoPath):
                self.ordersWriteToFile(self.photo, photoPath)

            os.startfile(os.path.abspath(os.getcwd()) + "/" + photoPath, 'open')

            con.close()

        # except (Exception, psycopg2.Error) as error:
        #     print("Error while fetching data from PostgreSQL", error)
        #     msg = QMessageBox()
        #     msg.setWindowTitle("ERROR...")
        #     msg.setText(f"Please first select ROW you want to open.")
        #     msg.setIcon(QMessageBox.Warning)
        #     msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        #
        #     style_gray.msgsheetstyle(msg)
        #
        #     x = msg.exec_()

    def MainClose(self):
        """exit app"""
        self.destroy()


class orderUpdate(QDialog):
    """double mouse click table"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 1000, 431)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Order App', 'Update1')
        # pozition and size
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
        self.ordersDetails()
        self.widgets()
        self.layouts()

    def ordersDetails(self):
        global ordersId

        conn = psycopg2.connect(
            **params
        )

        cur = conn.cursor()

        cur.execute("""SELECT * FROM orders WHERE ID=%s""", (ordersId,))
        orders = cur.fetchone()

        conn.close()

        self.uzsakymasCompany = orders[1]
        self.uzsakymasClient = orders[2]
        self.uzsakymasPhone = orders[3]
        self.uzsakymasName = orders[4]
        self.uzsakymasTerm = orders[5]
        self.uzsakymasStatus = orders[6]
        self.uzsakymasComments = orders[7]
        self.uzsakymasFolder = orders[8]
        self.uzsakymasFile = orders[9]
        # self.uzsakymasUpdate_date = uzsakymas[10]
        self.filename = orders[12]
        self.photo = orders[13]
        self.filetype = orders[14]

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

        self.companyCombo1 = QComboBox()
        self.companyCombo1.setEditable(True)
        self.companyCombo1.addItems(
            list_company)
        self.companyCombo1.setCurrentText(self.uzsakymasCompany)
        self.companyCombo1.setFont(QFont("Times", 12))

        self.clientCombo1 = QComboBox()
        self.clientCombo1.setEditable(True)
        self.clientCombo1.addItems(list_client)
        self.clientCombo1.setCurrentText(self.uzsakymasClient)
        self.clientCombo1.setFont(QFont("Times", 12))

        self.phoneCombo1 = QComboBox()
        self.phoneCombo1.setEditable(True)
        self.phoneCombo1.setPlaceholderText('Text')
        self.phoneCombo1.addItems(list_phone)
        self.phoneCombo1.setCurrentText(self.uzsakymasPhone)
        self.phoneCombo1.setFont(QFont("Times", 12))

        self.nameCombo1 = QComboBox()
        self.nameCombo1.setEditable(True)
        self.nameCombo1.setPlaceholderText('Text')
        self.nameCombo1.addItems(list_name)
        self.nameCombo1.setCurrentText(self.uzsakymasName)
        self.nameCombo1.setFont(QFont("Times", 12))

        self.termEntry1 = QComboBox()
        self.termEntry1.addItems(["-", "+"])
        self.termEntry1.setEditable(True)
        self.termEntry1.setCurrentText(self.uzsakymasTerm)
        self.termEntry1.setFont(QFont("Times", 12))

        self.statusCombo1 = QComboBox()
        self.statusCombo1.addItems(['FINISHED', 'IN PROCESS'])
        self.statusCombo1.setEditable(True)
        self.statusCombo1.setCurrentText(self.uzsakymasStatus)
        self.statusCombo1.setFont(QFont("Times", 12))

        self.commentsEntry1 = QTextEdit()
        self.commentsEntry1.setText(self.uzsakymasComments)
        self.commentsEntry1.setFont(QFont("Times", 12))

        self.locEntry = QLineEdit()
        self.locEntry.setText(self.uzsakymasFolder)
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.folderBtn = QPushButton("LINK TO FOLDER")
        self.folderBtn.setFixedHeight(25)
        self.folderBtn.clicked.connect(self.OpenFolderDialog)
        self.folderBtn.setFont(QFont("Times", 10))

        self.ListEntry1 = QLineEdit()
        self.ListEntry1.setText(self.uzsakymasFile)
        self.ListEntry1.setReadOnly(True)
        self.ListEntry1.setFont(QFont("Times", 12))
        self.ListEntry1.setStyleSheet("QLineEdit{background: darkgrey;}")

        self.fileBtn = QPushButton("CHANGE FILE")
        self.fileBtn.setFixedHeight(25)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("CHANGE DATE")
        self.dateBtn.setFixedWidth(110)
        self.dateBtn.setFixedHeight(25)
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFont(QFont("Times", 10))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(25)
        self.okBtn.clicked.connect(self.updateorders)
        self.okBtn.setFont(QFont("Times", 10))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(25)
        self.cancelBtn.clicked.connect(self.cancelorders)
        self.cancelBtn.setFont(QFont("Times", 10))

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()

        # self.qhbox1 = QHBoxLayout()
        # self.qhbox1.addWidget(self.locEntry)
        # self.qhbox1.addWidget(self.breziniaiBtn)
        #
        # self.qhbox2 = QHBoxLayout()
        # self.qhbox2.addWidget(self.ListEntry1)
        # self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.termEntry1)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("Company:"), self.companyCombo1)
        self.widgetLayout.addRow(QLabel("Client:"), self.clientCombo1)
        self.widgetLayout.addRow(QLabel("Phone Number:"), self.phoneCombo1)
        self.widgetLayout.addRow(QLabel("Order Name:"), self.nameCombo1)
        self.widgetLayout.addRow(QLabel("Order Term:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("Order Status:"), self.statusCombo1)
        self.widgetLayout.addRow(QLabel("Add Folder:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.folderBtn)
        self.widgetLayout.addRow(QLabel("Add File:"), self.ListEntry1)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("Comments:"))
        self.widgetLayout2.addRow(self.commentsEntry1)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        self.mainLayout1.addWidget(self.widgetFrame, 37)
        self.mainLayout1.addWidget(self.widgetFrame2, 63)

        self.mainLayout.addLayout(self.mainLayout1)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def terminasCalendar(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(25)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QWidget()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(780, 280, 350, 350)
        self.calendarWindow.setWindowTitle('ORDER TERM')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        style_gray.QCalendarstyle(self)
        self.calendarWindow.show()

        # @QtCore.pyqtSlot(QtCore.QDate)
        def get_date(qDate):
            if qDate.day() <= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            elif qDate.day() <= 9 and qDate.month() >= 10:
                date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            elif qDate.day() >= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            else:
                date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            self.calendarWindow.close()

        self.cal.clicked.connect(get_date)

    def cal_cancel(self):
        self.calendarWindow.close()

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

        self.ListEntry1.setText(f"{justfilename}{filetype}")

    def updateorders(self):
        global ordersId

        company1 = self.companyCombo1.currentText().upper()
        client1 = self.clientCombo1.currentText().upper()
        phone1 = self.phoneCombo1.currentText().upper()
        name1 = self.nameCombo1.currentText()
        term1 = self.termEntry1.currentText()
        status1 = self.statusCombo1.currentText().upper()
        comments1 = str(self.commentsEntry1.toPlainText())
        folder1 = self.locEntry.text()
        file1 = self.ListEntry1.text()
        update_date1 = self.update_date.text()

        filename1 = self.ListFileName.text()
        blobPhoto1 = self.convertToBinaryDataFile(self.ListDir.text())
        filetype1 = self.ListFileType.text()
        filedir1 = self.ListDir.text()

        term_entry = ""

        if term1 != term_entry:
            try:
                if self.ListDir.text() != "":
                    conn = psycopg2.connect(
                        **params
                    )

                    cur = conn.cursor()

                    query = "UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, " \
                            "order_term = %s, status = %s, comments = %s, order_folder = %s, order_file = %s, " \
                            "update_date = %s, filename = %s, photo = %s, filetype = %s, filedir = %s " \
                            "where id = %s"
                    cur.execute(query, (company1, client1, phone1, name1, term1, status1, comments1,
                                        folder1, file1, update_date1, filename1, blobPhoto1, filetype1, filedir1,
                                        ordersId))
                    conn.commit()
                    conn.close()

                else:
                    conn = psycopg2.connect(
                        **params
                    )

                    cur = conn.cursor()

                    query = "UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, " \
                            "order_term = %s, status = %s, comments = %s, order_folder = %s, order_file = %s, " \
                            "update_date = %s where id = %s"
                    cur.execute(query, (company1, client1, phone1, name1, term1, status1, comments1,
                                        folder1, file1, update_date1, ordersId))
                    conn.commit()
                    conn.close()

            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText(f"Error while fetching data from PostgreSQL: {error}")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/icon.ico'))

                style_gray.msgsheetstyle(msg)

                x = msg.exec_()


        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("ORDER TERM can't be empty...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/icon.ico'))

            style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelorders(self):
        self.close()


def main():
    App = QApplication(sys.argv)

    window = MainMenu()

    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
