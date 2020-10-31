    
# This file set QT windows and defines all signals and slots

from PyQt5 import QtWidgets,QtCore,QtGui
from GraphGenerator import *
from datetime import datetime
import os.path
from progress_bar import *
from web_scraping import *
import xlsxwriter
import socket
 
from DataTransferer import *

class Ui_MainWindow(object): 
    def setupUi(self, MainWindow):
        # position parameters
        self.right_pos_x = 420
        self.loop_pos_y = 360
        # initialisation of the qwidget position and size
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        
    
        self.btn_txt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_txt.setObjectName("btn_txt")
        self.btn_txt.setToolTip('Select TXT file which contains run IDs')
     

        self.btn_generate = QtWidgets.QPushButton(self.centralwidget)
        self.btn_generate.setGeometry(QtCore.QRect(600, 500, 150, 30))
        self.btn_generate.setToolTip('Generate PDF file which contains all graphs selected')  


        self.btn_select_loop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_select_loop.setGeometry(QtCore.QRect(self.right_pos_x, self.loop_pos_y, 112, 32))
        self.btn_select_loop.setDisabled(True)
        self.btn_select_loop.setToolTip('Select loop(s) from all loops provided')  
        

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(20, 40, 391, 45))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.title.setFont(font)
        self.title.setTextFormat(QtCore.Qt.AutoText)
        self.title.setObjectName("titlel")

        self.introl = QtWidgets.QLabel(self.centralwidget)
        self.introl.setGeometry(QtCore.QRect(20, 80, 700, 31))
        self.introl.setWordWrap(True)
        self.introl.setObjectName("introl")
        
        self.selectgraphl = QtWidgets.QLabel(self.centralwidget)
        self.selectgraphl.setGeometry(QtCore.QRect(20, 220, 700, 31))
        self.selectgraphl.setWordWrap(True)
        self.selectgraphl.setObjectName("selectgraphl")

        self.othercolumnl = QtWidgets.QLabel(self.centralwidget)
        self.othercolumnl.setGeometry(QtCore.QRect(20, 410, 700, 31))
        self.othercolumnl.setWordWrap(True)
        self.othercolumnl.setObjectName("othercolumnl")
        


        self.path_line2 = QtWidgets.QLineEdit(self.centralwidget)
        self.path_line2.setObjectName("path_line2")
        self.path_line2.clearFocus()

        
        self.HLayoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.HLayoutWidget1.setGeometry(QtCore.QRect(20, 90, 700, 70))
        self.HLayout1 = QtWidgets.QHBoxLayout(self.HLayoutWidget1)
        self.HLayout1.setContentsMargins(0, 0, 0, 0)
        
        self.HLayout1.addWidget(self.btn_txt)
        self.HLayout1.addWidget(self.path_line2)

        self.HLayoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.HLayoutWidget2.setGeometry(QtCore.QRect(150, 150, 500, 60))
        self.HLayout2 = QtWidgets.QHBoxLayout(self.HLayoutWidget2)
        self.HLayout2.setContentsMargins(0, 0, 0, 0)
        
        self.text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(180, 153, 431, 30))
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setText("Search online")

        self.VLayoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.VLayoutWidget4.setGeometry(QtCore.QRect(300, 153, 100, 120))
        self.VLayout4 = QtWidgets.QVBoxLayout(self.VLayoutWidget4)
        self.VLayout4.setContentsMargins(0, 0, 0, 0)
        self.VLayout4.addWidget(self.btn_search)

        self.progress_bar = ProgressBarWidget()
        self.VLayout4.addWidget(self.progress_bar)
        
        self.progress_bar.setHidden(True)

        self.HLayout2.addWidget(self.text_edit)
        self.text_edit.setToolTip('You can add/delete RunIDs if needed.\nRunIDs should be seperated by ",".')
        self.HLayout2.addWidget(self.VLayoutWidget4)
        self.btn_search.clicked.connect(self.search_online)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 275, 200, 130))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.max_per_page_combo = QtWidgets.QComboBox(self.centralwidget)
        self.max_per_page_combo.setGeometry(QtCore.QRect(self.right_pos_x, 250, 91, 32))
        self.max_per_page_combo.setObjectName("max_per_page_combo")
        self.max_per_page_combo.addItem("1")
        self.max_per_page_combo.addItem("2")
        self.max_per_page_combo.addItem("3")
        self.max_per_page_combo.addItem("4")
        self.max_per_page_combo.addItem("5")
        self.max_per_page_combo.addItem("6")
        self.max_per_page_combo.setCurrentIndex(5)

        self.maxl = QtWidgets.QLabel(self.centralwidget)
        self.maxl.setGeometry(QtCore.QRect(420, 220, 300, 31))
        self.maxl.setObjectName("maxl")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(420, 330, 300, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.loopl = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.loopl.setObjectName("loopl")
        self.horizontalLayout.addWidget(self.loopl)

        # list of graph types
        graph_types = ['Status','Belt bracket on track','Longitudinal load','Recliner torque','Front bracket load','Rear brackets load']
        self.cb = []
        # initialisation of list of selected graphs (False means unselected, True means selected)
        self.cb_selected = [False]*len(graph_types)

        # create checkbox widget for each graph type
        for i in range(len(graph_types)):
            widget = QtWidgets.QCheckBox(graph_types[i], self.verticalLayoutWidget)
            widget.setObjectName("cb_"+graph_types[i])
            self.cb.append(widget)
        # add them to the vertical layout
        for cb_obj in self.cb:
            self.verticalLayout.addWidget(cb_obj)

        # create checkbox "select all"
        self.cb_all = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_all.setGeometry(QtCore.QRect(50, 250, 160, 20))
        self.cb_all.setObjectName("checkbox_all")
        
        #create a model for listview
        self.listview = QListView()

        self.VLayoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.VLayoutWidget5.setGeometry(QtCore.QRect(70, 460, 200, 100))
        self.VLayout5 = QtWidgets.QVBoxLayout(self.VLayoutWidget5)
        self.VLayout5.setContentsMargins(0, 0, 0, 0)
        self.VLayout5.addWidget(self.listview)

        self.cb_all2 = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_all2.setGeometry(QtCore.QRect(50, 440, 160, 20))
        self.cb_all2.setObjectName("checkbox_all2")
        self.cb_all2.setDisabled(True)



        # menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menuFile = QtWidgets.QMenu(self.menubar)

        self.menuEdit = QtWidgets.QMenu(self.menubar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        # Faurecia logo
        logo = QLabel(self.centralwidget)
        pixmap = QtGui.QPixmap('./pic/logo_faurecia.png')
        pixmap = pixmap.scaled(200,200, QtCore.Qt.KeepAspectRatio)
        logo.setPixmap(pixmap)
        logo.move(570,30)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # signals & slots
        self.tmp_excel_path = ''
        self.btn_txt.clicked.connect(self.get_txt_file)
        self.cb_all.clicked.connect(self.select_all_clicked)
        self.cb_all2.clicked.connect(self.select_all_clicked2)

        for cb in self.cb:
            cb.stateChanged.connect(self.cb_change_state)   
        self.btn_select_loop.clicked.connect(self.btn_select_loop_clicked)
        self.text_edit.textChanged.connect(self.runid_modified)
        self.btn_generate.clicked.connect(self.generate_charts)
        

        
        self.cb_all.setChecked(True)
        self.select_all_clicked()
        # some default settings

        self.btn_search.setDisabled(True)

        # other useful parameters
        self.selected_loop = []
        self.runIDs = []
        self.otheritems = []
        self.btn_search_toggled = False
        self.grasper = DataGrasper()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "THC One Click"))
        self.btn_txt.setText(_translate("MainWindow","Select txt file"))
        self.btn_generate.setText(_translate("MainWindow", "Generate PDF"))
        self.title.setText(_translate("MainWindow", "THC One Click"))
        self.introl.setText(_translate("MainWindow", "Select your txt file(Runids),then click 'Search Online'.Excels will be created in your Desktop,in folder 'THC_output_file'.\nYou can also click Generate PDF to get quick charts.   !!please CLOSE your excel before run programe!!" ))
        self.cb_all.setText(_translate("MainWindow", "Select all"))
        self.cb_all2.setText(_translate("MainWindow", "Select all"))
        self.maxl.setText(_translate("MainWindow", "Number of graphs per page: "))
        self.loopl.setText(_translate("MainWindow", "Selected loop(s): "))
        self.selectgraphl.setText(_translate("MainWindow", "Select all the graphs that you would like to create:"))
        self.othercolumnl.setText(_translate("MainWindow", "Select other columns if you want:"))
        self.btn_select_loop.setText(_translate("MainWindow", "Select loop(s)"))
        
    def select_all_clicked(self):
        if self.cb_all.isChecked():
            for cb in self.cb:
                cb.setChecked(True)
        else:
            for cb in self.cb:
                cb.setChecked(False)
       
    def select_all_clicked2(self):
        cpt = 0
        if self.cb_all2.isChecked(): 
            print('cb_all2 ischecked')
            while self.model.item(cpt)!=None:
                check = Qt.Checked
                self.model.item(cpt).setCheckState(check)
                cpt+=1
        else:
            print('cb_all2 is not checked')
            while self.model.item(cpt)!=None:
                check = Qt.Unchecked
                self.model.item(cpt).setCheckState(check)
                cpt+=1
        

    def cb_change_state(self):
        # create 2 variables 
        self.all_selected = True
        self.all_unselected = True
        for cb in self.cb:
            if cb.isChecked()==False:
                self.all_selected = False
            else:
                self.all_unselected = False

        # change state of the checkbox "select all" based on the values of 2 variables
        if not self.all_selected and not self.all_unselected:
            self.cb_all.setTristate(True)
            self.cb_all.setCheckState(Qt.PartiallyChecked)
        elif self.all_selected:
            self.cb_all.setCheckState(Qt.Unchecked)
            self.cb_all.setChecked(True)
        else:
            self.cb_all.setChecked(False)
 

    def get_txt_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,"getOpenFileName",sys.path[0],"Text Files (*.txt)")
        print(file)
        # if user clicked cancel, nothing happens
        if(file[0]==''):
            return
        self.path_line2.setText(file[0])
        
        IDs = self.grasper.open_txt_file(file[0])
        text = self.text_edit.toPlainText()
        if (text!=''):
            text = self.text_edit.toPlainText().replace(' ','')
            self.runIDs = text.split (",")
            print(self.runIDs)
        else:
            self.runIDs = []

        self.runIDs = list(set().union(IDs,self.runIDs))
        print(self.runIDs)
        text = ', '.join(self.runIDs)
        self.text_edit.setPlainText(text)



    def setDefaultLoop(self,path):
        loop_list = self.get_all_loop(path)
        self.selected_loop = [loop_list[0]]
        loop_str = self.selected_loop[0]
        self.loopl = QtWidgets.QLabel(loop_str,self.centralwidget)
        self.horizontalLayout.addWidget(self.loopl)
        print(self.selected_loop)


    # get all current loops in the file
    def get_all_loop(self, path):
        # create generator object
        self.gen = GraphGenerator(path)
        df_selected = self.gen.df_origin[['OEM','project_name','design_loop']]
        dic_loop = df_selected.groupby(['design_loop']).apply(list).to_dict()
        
        self.clear_all_loop()
        loop_list = list(dic_loop.keys())
        return loop_list

    
        
    def clear_all_loop(self): 
        for i in range(1,self.horizontalLayout.count()): 
            self.horizontalLayout.itemAt(i).widget().close()   # clear all previously selected loops
        self.selected_loop = []

     
    def runid_modified(self):
        self.clear_all_loop()
        print(self.text_edit.toPlainText())
        if self.text_edit.toPlainText() != '':
            self.btn_search.setDisabled(False)
        else:
            self.btn_search.setDisabled(True)


    def search_online(self):
        if self.btn_search_toggled == False:
            print('search clicked')
            self.btn_search_toggled = True
            self.btn_search.setText('Cancel')
            
            text = self.text_edit.toPlainText().replace(' ','')
            text = text.rstrip(',')
            text = text.lstrip(',')
            
            self.runIDs = text.split (",")
            self.runIDs = [runid.strip() for runid in self.runIDs]

            self.cb_all2.setChecked(False)
            self.cb_all2.setDisabled(True)
            self.listview.setDisabled(True)
            self.otheritems.clear()

            self.worker = BackendQThread(self.execute_this_fn1)
            self.worker.signals.result.connect(self.print_output)
            self.worker.signals.result.connect(self.thread_completed)
            self.worker.signals.finished.connect(self.thread_finished)
            
            self.worker.signals.error.connect(self.pop_error)
            self.worker.start()
            self.progress_bar.onStart()

        else:
            print('cancel clicked')
            self.btn_search_toggled=False
            self.btn_search.setText('Search')
            self.worker.terminate()
            self.progress_bar.stop()
            self.progress_bar.setHidden(True)

    def execute_this_fn1(self):
        print('execute_this_fn1')
        self.grasper.search_online_by_runID(self.runIDs)
        print("RunIDs:", self.runIDs)
        self.tmp_excel_path = self.grasper.generate_xml()
        self.btn_search.setText('Search')
        return 0


    def print_output(self, s):
        print(s)


    def pop_error(self, e):
        print("*************************************************************")
        self.progress_bar.setHidden(True)
        if type(e) == AttributeError:
            msgbox = MyMessageBox(QMessageBox.Critical,'RunID not found','Please check the RunID')
            msgbox.exec()
        elif type(e) == requests.exceptions.ConnectionError:
            msgbox = MyMessageBox(QMessageBox.Critical,'ConnectionError','Please check your internet connection')
            msgbox.setDetailedText(str(e))
            msgbox.exec()
        elif type(e) == xlsxwriter.exceptions.FileCreateError:
            msgbox = MyMessageBox(QMessageBox.Critical,'FileCreateError','Unable to create excel file, please close temperate excel file')
            msgbox.setDetailedText(str(e))
            msgbox.exec() 
        else:
            msgbox = MyMessageBox(QMessageBox.Critical,'Unexpected error','Please restart the program')
            msgbox.exec()

    def thread_completed(self):
        self.btn_select_loop.setDisabled(False)
        self.cb_all2.setDisabled(False)
        self.listview.setDisabled(False)
        try:
            self.Transferer = DataTransferer(raw_file_name = self.tmp_excel_path)
            msg_list = self.setOtherColumn()
            self.regular_excel_path = self.Transferer.generate_reg_excel()
            self.setDefaultLoop(self.regular_excel_path)            
        except xlsxwriter.exceptions.FileCreateError as e:
            msgbox = MyMessageBox(QMessageBox.Critical,'FileCreateError','Unable to create excel file, please close regular excel file:\n'+self.regular_excel_path)
            msgbox.exec()

        warning_msg = "\n".join(msg_list)
        print(warning_msg)
        if len(warning_msg) == 0:
            warning_msg = "All keywords matched successfully!"
        
        msgbox = MyMessageBox(QMessageBox.Information,'Complete','Excel files generated successfully')
        msgbox.setDetailedText(warning_msg)
        msgbox.exec()
    
    def thread_finished(self):
        print("THREAD finished!")
        self.progress_bar.stopend()
        self.progress_bar.stop()
        self.btn_search_toggled = False
        self.btn_search.setText('Search')


    def btn_select_loop_clicked(self):
        self.select_loop()


    def select_loop(self):
        print("select loop button clicked")
        # if there is no temporary excel file => error
        if not os.path.isfile(self.regular_excel_path):
            msgbox = MyMessageBox(QMessageBox.Critical,'Missing file','File does not exist!')
            msgbox.setDetailedText("Can not find file from path below:\n"+self.regular_excel_path)
            msgbox.exec()
            return
        loop_list = self.get_all_loop(self.regular_excel_path)
        form = ChecklistDialog("All Loops",loop_list, checked=True)
        if form.exec_() == QtWidgets.QDialog.Accepted:
            self.selected_loop = [str(s) for s in form.choices]
            loop_str = ', '.join(self.selected_loop)
            print("loop:",loop_str)
            self.loopl = QtWidgets.QLabel(loop_str,self.centralwidget)
            self.horizontalLayout.addWidget(self.loopl)

            if(len(self.selected_loop)>1):
                print("more than one loop")

    def setOtherColumn(self):
        
        all_criteria, uncommon_criterias, msg_list = self.Transferer.getInfo()
        print(all_criteria, uncommon_criterias)
        #create a model for listview 
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self.setItems)

        for item in uncommon_criterias:            
            item = QtGui.QStandardItem(item)
            check = Qt.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            self.model.appendRow(item)

        self.listview.setModel(self.model)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cb_all2.setDisabled(False)
        return msg_list

        

    def setItems(self,item):
        if item.checkState() == QtCore.Qt.Checked:
            self.otheritems.append(item)
        if item.checkState() == QtCore.Qt.Unchecked:
            self.otheritems.remove(item)

        print('len(self.otheritems):',len(self.otheritems))
        print('self.model.rowCount():',self.model.rowCount())
    
        if len(self.otheritems) == 0:
            self.cb_all2.setCheckState(Qt.Unchecked)
        elif len(self.otheritems) == self.model.rowCount():
            self.cb_all2.setCheckState(Qt.Checked)
        else:
            print('there is a item checked')
            self.cb_all2.setCheckState(Qt.PartiallyChecked)

    def all_prepared(self):
        # if file path undefined =>warning 
        if not hasattr(self, 'regular_excel_path') or self.regular_excel_path == '':
            QMessageBox.warning(self.centralwidget,"Missing path","Please execute search first!")
            return False
        # if file can't be found => warning
        elif not os.path.isfile(self.regular_excel_path):
            msgbox = MyMessageBox(QMessageBox.Critical,'Missing file','File does not exist!')
            msgbox.setDetailedText("Can not find file from path below:\n"+self.regular_excel_path)
            msgbox.exec()
            return False
        # if no loop has been selected => warning
        elif len(self.selected_loop)==0:
            QMessageBox.warning(self.centralwidget,"Missing loop","Please select at least one loop")
            return False
        # if none of the graph has been chosen => warning
        elif not hasattr(self, 'all_unselected') or self.all_unselected == True:
            QMessageBox.warning(self.centralwidget,"Missing graph","Please select at least one graph")
            return False
        return True

    def generate_charts(self):
        if self.all_prepared():
            for i in range(len(self.cb)):
                self.cb_selected[i] =  self.cb[i].isChecked()

            max_per_page = int(self.max_per_page_combo.currentText())
            print("Generating graphs...")
            filename = "THC_Summary_Report_"+datetime.today().strftime('%d_%m_%Y')+".pdf"
            desk = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\THC_output_file'     #declear directory where we want export xlsx file.
            filepath = desk + '\\'+ filename
            save_path =  QtWidgets.QFileDialog.getSaveFileName(self.centralwidget,"Select a path to save the file...",filepath,"")
            if save_path[1] != '':
                save_path = save_path[0]
                otheritems_list = [x.text() for x in self.otheritems]   # convert QStandardItem to string
                try:
                    self.gen.generate_pdf(self.cb_selected, self.selected_loop,otheritems_list, save_path, max_per_page = max_per_page)
                except PermissionError:
                    QMessageBox.warning(self.centralwidget,"PermissionError","Please close the PDF file!")
                    return   
                msgBox = MyMessageBox(self.centralwidget)
                msgBox.setWindowTitle("File generated")
                msgBox.setText("File generated successfully\n")
                
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec()
                print("PDF generated")

class ChecklistDialog(QDialog):
    def __init__(
        self,
        name,
        stringlist=None,
        checked=False,
        icon=None,
        parent=None,
        ):
        super(ChecklistDialog, self).__init__(parent)

        self.name = name
        self.icon = icon
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()

        for string in stringlist:
            item = QtGui.QStandardItem(string)
            item.setCheckable(True)
            check = \
                (QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked)
            item.setCheckState(check)
            self.model.appendRow(item)

        self.listView.setModel(self.model)

        self.okButton = QtWidgets.QPushButton('OK')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.selectButton = QtWidgets.QPushButton('Select All')
        self.unselectButton = QtWidgets.QPushButton('Unselect All')

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.selectButton)
        hbox.addWidget(self.unselectButton)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setWindowTitle(self.name)
        if self.icon:
            self.setWindowIcon(self.icon)

        self.okButton.clicked.connect(self.onAccepted)
        self.cancelButton.clicked.connect(self.reject)
        self.selectButton.clicked.connect(self.select)
        self.unselectButton.clicked.connect(self.unselect)

    def onAccepted(self):
        self.choices = [self.model.item(i).text() for i in
                        range(self.model.rowCount())
                        if self.model.item(i).checkState()
                        == QtCore.Qt.Checked]
        self.accept()

    def select(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Checked)

    def unselect(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)

class MyMessageBox(QMessageBox):

    # This is a much better way to extend __init__
    def __init__(self, *args, **kwargs):            
        super(MyMessageBox, self).__init__(*args, **kwargs)
        # Anything else you want goes below

    # We only need to extend resizeEvent, not every event.
    def resizeEvent(self, event):
        result = super(MyMessageBox, self).resizeEvent(event)
        details_box = self.findChild(QtWidgets.QTextEdit)
        if details_box is not None:
            details_box.setFixedSize(details_box.sizeHint())

        return result




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QtGui.QPixmap('./pic/launch_logo.png')
    pixmap = pixmap.scaled(300,200, QtCore.Qt.KeepAspectRatio)
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())






