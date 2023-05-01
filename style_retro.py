def SheetStyle(self):
    """app style"""
    self.setStyleSheet("""QWidget{
                            background-color:#F3DEBA;
                            }
                            
                            
                            QGroupBox{
                            background-color: #F3DEBA;
                            border-top: 1px solid black;
                            border-bottom: 1px solid black;
                            margin-top: 10px;
                            padding: 3px;
                            }

                            QGroupBox::title {
                            color: black;
                            bottom: 10px;
                            subcontrol-position: top;
                            }

                            QScrollBar::vertical{
                            background-color:#675D50;
                            width:10px;
                            padding-top:24px;
                            }

                            QScrollBar::sub-page:vertical{
                            background: #F3DEBA;
                            }

                            QScrollBar::add-page:vertical{
                            background: #F3DEBA;
                            }
                            
                            QScrollBar::sub-page:horizontal{
                            background: #F3DEBA;
                            }
                            
                            QScrollBar::add-page:horizontal{
                            background: #F3DEBA;
                            }

                            QScrollBar::handle{
                            background-color: #675D50;
                            }

                            QScrollBar::sub-line:vertical {
                            height: 22px;
                            background-color: #675D50;
                            border-bottom:1px solid black;
                            border-left:1px solid black;
                            }
                            
                            QTreeView::corner {
                            background-color: #675D50;
                            }
                            

                            QTableWidget{
                            background: white;
                            gridline-color:black;
                            border:1px solid black;
                            }

                            QTableWidget::item:hover{
                            background:#ABC4AA;
                            color: white;
                            }

                            QTableWidget::item:selected{
                            background:#A9907E;
                            color:white;
                            }
                            
                            QTableWidget::corner {
                            background-color: #675D50;
                            }

                            QHeaderView{
                            background-color:#9F8772;
                            }

                            QHeaderView::section{
                            background:#675D50;
                            color:white;
                            }

                            QHeaderView::section:selected{
                            background:#A9907E;
                            color:white;
                            }

                            QHeaderView::section:checked{
                            background-color: #675D50;
                            font: normal;
                            }

                            QTableCornerButton::section{
                            background:#9F8772;
                            border:0.5px solid black;
                            }



                            QTreeWidget{
                            background: white;
                            padding: 3%;
                            }

                            QTreeWidget::item:hover{
                            background:#ABC4AA;
                            color: white;
                            }

                            QTreeWidget::item:selected{
                            background:#A9907E;
                            color:white;
                            border: 1px solid black;
                            }



                            QPushButton{
                            background-color:#675D50;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            }

                            QPushButton::hover{
                            background-color:#ABC4AA;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:#675D50;
                            color:white;
                            }



                            QLineEdit{
                            background-color:white;
                            color:black;
                            border:1px solid black;
                            padding:2px;
                            }



                            QMenuBar{
                            background-color: #675D50;
                            color: white;
                            border:1px solid black;
                            }

                            QMenuBar::item{
                            background-color: #675D50;
                            color: white;
                            padding:5px;
                            }

                            QMenuBar::item::selected{
                            background-color: #ABC4AA;
                            color: white;
                            }

                            QMenu{
                            background-color: #675D50;
                            color: white;
                            border:1px solid black;
                            padding:3px;
                            }

                            QMenu::selected{
                            background-color: #ABC4AA;
                            color: white;
                            }

                            QMenu::separator{
                            background-color:black;
                            margin:4px;
                            }



                            QToolBar{
                            background-color:#675D50;
                            color:dark#9F8772;
                            border:1px solid black;
                            }

                            QToolBar::separator{
                            background-color:black;
                            margin:3px;
                            margin-left:2px;
                            }

                            QToolButton{
                            background-color:#675D50;
                            color:white;
                            padding:2px;
                            }

                            QToolButton::hover{
                            background-color:#ABC4AA;
                            color:white;
                            }
                        
                        
                            QProgressBar {
                            margin-top:-1px;
                            margin-bottom:-1px;
                            }
                            
                            QProgressBar::chunk {
                            background-color: #ABC4AA;
                            }
                            """)


def msgsheetstyle(msg):
    msg.setStyleSheet("""QMessageBox{
                            background-color:#F3DEBA;
                            }



                            QPushButton{
                            background-color:#675D50;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            min-Width:60px;
                            }

                            QPushButton::hover{
                            background-color:#ABC4AA;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }

                            """)


#
#
def mboxsheetstyle(mbox):
    mbox.setStyleSheet("""QMessageBox{
                            background-color:#F3DEBA;
                            }



                            QPushButton{
                            background-color:#675D50;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            min-Width:110px;
                            }

                            QPushButton::hover{
                            background-color:#ABC4AA;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }

                            """)


#
def QDialogsheetstyle(self):
    self.setStyleSheet("""QDialog{
                            background-color:#F3DEBA;
                            }

                            QGroupBox{
                            background-color: #F3DEBA;
                            border: 1px solid black;
                            margin-top: 10px;
                            padding: 10px;;
                            }

                            QGroupBox::title {
                            color: black;
                            bottom: 10px;
                            subcontrol-position: top;
                            }

                            QPushButton{
                            background-color:#675D50;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::hover{
                            background-color:#ABC4AA;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }
                            
                            """)


def QCalendarstyle(self):
    self.calendarWindow.setStyleSheet("""QPushButton{
                                        background-color:#675D50;
                                        color:white;
                                        border-radius:3px;
                                        border:1px solid black;
                                        padding:3px;
                                        }
            
                                        QPushButton::hover{
                                        background-color:#ABC4AA;
                                        color:white;
                                        border:1px solid black;
                                        }
            
                                        QPushButton::pressed{
                                        background-color:#675D50;
                                        color:white;
                                        }
            
                                        """)
