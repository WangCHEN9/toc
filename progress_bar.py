import sys
from PyQt5.Qt import QThread, QApplication, QWidget, QVBoxLayout
from PyQt5.Qt import QTimer, QObject, QPushButton, QLabel, pyqtSignal
import time


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback

class ProgressBarWidget(QWidget):

    def __init__(self, parent=None):
        super(ProgressBarWidget, self).__init__(parent)
        layout = QVBoxLayout(self)       

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
        layout.addWidget(self.progressBar)
        self.myLongTask = TaskThread()
        self.myLongTask.notifyProgress.connect(self.onProgress)
        
        self.isrunning = True

        self.currentper = 0
 

    def onStart(self):
        print('current:',self.currentper)
        self.setHidden(False)
        if self.currentper==100:
            self.myLongTask.current = 0

        self.isrunning = True
        self.myLongTask.start()

    def onProgress(self, i):
        if self.isrunning:
            self.progressBar.setValue(i)
            self.currentper = i

    def stopend(self):
        if self.currentper < 99:
            self.temp = 100 - self.currentper
            while(self.temp):
                self.onProgress(1 + self.currentper)
                self.temp-=1
        else:
            self.onProgress(100)

    def stop(self):
        self.isrunning = False
        self.myLongTask.terminate()


class TaskThread(QThread):
    notifyProgress = pyqtSignal(int)
    def __init__(self, parent=None):
        super(TaskThread, self).__init__()  

    def run(self):
        self.current = 0
        while self.current <99:
            self.notifyProgress.emit(self.current)
            time.sleep(25*1/(100-self.current))
            self.current +=1


class BackendQThread(QThread):
    """
        Class who create a QThread to trigger requests
    """

    quit_thread = pyqtSignal(name='close_thread')

    def __init__(self, fn, *args, **kwargs):
        super(BackendQThread, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        """
        Run the actions depending on the selected task

        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            print(type(e))
            traceback.print_exc()
            self.signals.error.emit(e)
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
            pass


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

