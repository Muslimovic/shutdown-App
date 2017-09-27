from worker import Worker
import subprocess
from PyQt5 import QtWidgets, QtCore
import gui
import time, datetime

class App(QtWidgets.QMainWindow,gui.Ui_MainWindow):
    def __init__(self):
        super(App,self).__init__() # The App Class become all variables and methods from Ui_MainWindow
        self.setupUi(self) # Method from Ui_MainWindow class, initialize all elements on the app window
        self.msg = QtWidgets.QMessageBox() # Warning and Information Box
        self.show() # Show the app window

        self.time = 0 # Time = after how many seconds the computer should shut down or restart

        # Set init Date and Time
        self.attime.setDateTime(QtCore.QDateTime.currentDateTime())
        # Set init Abort Button
        self.pB_abort.setEnabled(False)
        self.stop = False
        # Set init Text Fields
        self.lineE_option.setEnabled(False)
        self.lineE_seconds.setEnabled(False)

        ####################################################################################################
        # The commands in this box are the buttons on the window and after some button press the program
        # will come here to execute the method assigned to the pressed button.

        # Time Group (check buttons)
        self.cB_after.stateChanged.connect(self.selectTime1)
        self.cB_timestamp.stateChanged.connect(self.selectTime2)
        # Option Group (check buttons)
        self.cB_shutdown.stateChanged.connect(self.cbShutdown)
        self.cB_restart.stateChanged.connect(self.cbRestart)
        self.cB_logout.stateChanged.connect(self.cbLogout)
        # Start the shutdown or restart process (push button, start)
        self.pB_start.clicked.connect(self.start)
        # Abort the previous selected option (push button, abort)
        self.pB_abort.clicked.connect(self.abort)
        # Help Button
        self.actionAbouttheApp.triggered.connect(self.about)
        self.actionAppInfo.triggered.connect(self.info)

        ######################################################################################################

    def start(self):
        """
        The start method is assigned to the start button. After correct configuration of time and option group and
        pressed start button, the method will create a thread to execute the chosen option (target). If the configuration
        is not correct a warning message will come on with the error information.
        :return:
        """
        target = None # equals to option
        self.stop = False # abort status
        self.lineE_option.setEnabled(True)
        self.lineE_seconds.setEnabled(True)
        if self.cB_after.isChecked():
            self.time = eval(self.sB_hour.text())*3600 + eval(self.sB_minute.text())*60 + eval(self.sB_second.text())
        elif self.cB_timestamp.isChecked():
            self.time = self.intDateTime(self.attime) - int(time.time())
        elif not self.cB_after.isChecked() and not self.cB_timestamp.isChecked():
            self.msgBox(text="Please select the time!")

        if self.time < 0: # the time can not be in the past
            self.msgBox(text="Please select a timestamp in future!")
        else:
            if self.cB_shutdown.isChecked() and (self.cB_after.isChecked() or self.cB_timestamp.isChecked()):
                self.pB_start.setEnabled(False)
                self.pB_abort.setEnabled(True)
                target = self.shutdown
            elif self.cB_restart.isChecked() and (self.cB_after.isChecked() or self.cB_timestamp.isChecked()):
                self.pB_start.setEnabled(False)
                self.pB_abort.setEnabled(True)
                target = self.restart
            elif self.cB_logout.isChecked() and (self.cB_after.isChecked() or self.cB_timestamp.isChecked()):
                self.pB_start.setEnabled(False)
                self.pB_abort.setEnabled(True)
                target = self.logout
            elif not self.cB_restart.isChecked() and not self.cB_shutdown.isChecked() and not self.cB_logout.isChecked():
                self.lineE_option.setEnabled(False)
                self.lineE_seconds.setEnabled(False)
                self.msgBox(text="Please select one Option!")

        try:
            # Start new thread with the target function
            self.newTask(target=target)
        except:
            pass

    def about(self):
        """
        Shows the information about the developer
        :return:
        """
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setInformativeText("Developed by\n\t Mr. Muslimovic Jasmin BSc\nContact: jasmin_muslimovic@hotmail.com\n\t\tVienna, Austria")
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.show()
    def info(self):
        """
        Shows the main goal and how the app works
        :return:
        """
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        #self.msg.setText("text")
        self.msg.setInformativeText("If You want to turn off or restart your computer in the future and can not do this manually, the ShutDown App "
                                    "helps You to this. Just select after which time you want to turn Your computer off or select some timestamp at which you "
                                    "want to turn off or restart Your computer. At the bottom of the window you will see the option you had chosen and "
                                    "in how many seconds the computer will do the chosen option.\n\nYou can stop the app with the 'Abort' button and configure "
                                    "the time or option in case You did some mistake by setting one of them. The Version 0.0 of the ShutDown App works on"
                                    " Windows and the next Version will work also on other systems.")
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.show()
    def msgBox(self, text):
        """

        :param text: Message Box that shows warnings
        :return:
        """
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText(text)
        # self.msg.setInformativeText(str(result))
        self.msg.setWindowTitle("Warning")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.show()

    def cbShutdown(self):
        if self.cB_shutdown.isChecked()==True:
            # Disable the Restart Checkbox
            self.cB_restart.setChecked(False)
            self.cB_restart.setCheckable(False)
            self.cB_restart.setEnabled(False)
            # Disable the Logout Checkbox
            self.cB_logout.setChecked(False)
            self.cB_logout.setCheckable(False)
            self.cB_logout.setEnabled(False)
        elif self.cB_shutdown.isChecked()==False:
            # Enable the Restart Checkbox
            self.cB_restart.setCheckable(True)
            self.cB_restart.setEnabled(True)
            # Enable the Logout Checkbox
            self.cB_logout.setCheckable(True)
            self.cB_logout.setEnabled(True)
    def cbRestart(self):
        if self.cB_restart.isChecked()==True:
            # Disable the Shutdown Checkbox
            self.cB_shutdown.setChecked(False)
            self.cB_shutdown.setCheckable(False)
            self.cB_shutdown.setEnabled(False)
            # Disable the Logout Checkbox
            self.cB_logout.setChecked(False)
            self.cB_logout.setCheckable(False)
            self.cB_logout.setEnabled(False)
        elif self.cB_restart.isChecked()==False:
            # Enable the Shutdown Checkbox
            self.cB_shutdown.setCheckable(True)
            self.cB_shutdown.setEnabled(True)
            # Enable the Logout Checkbox
            self.cB_logout.setCheckable(True)
            self.cB_logout.setEnabled(True)
    def cbLogout(self):
        if self.cB_logout.isChecked()==True:
            # Disable the Shutdown Checkbox
            self.cB_shutdown.setChecked(False)
            self.cB_shutdown.setCheckable(False)
            self.cB_shutdown.setEnabled(False)
            # Disable the Restart Checkbox
            self.cB_restart.setChecked(False)
            self.cB_restart.setCheckable(False)
            self.cB_restart.setEnabled(False)
        elif self.cB_logout.isChecked()==False:
            # Enable the Shutdown Checkbox
            self.cB_shutdown.setCheckable(True)
            self.cB_shutdown.setEnabled(True)
            # Enable the Restart Checkbox
            self.cB_restart.setCheckable(True)
            self.cB_restart.setEnabled(True)


    def selectTime1(self):
        if self.cB_after.isChecked()==True:
            self.cB_timestamp.setChecked(False)
            self.cB_timestamp.setCheckable(False)
            self.cB_timestamp.setEnabled(False)
            self.attime.setEnabled(False)
        elif self.cB_after.isChecked()==False:
            self.cB_timestamp.setCheckable(True)
            self.cB_timestamp.setEnabled(True)
            self.attime.setEnabled(True)
    def selectTime2(self):
        if self.cB_timestamp.isChecked() == True:
            self.cB_after.setChecked(False)
            self.cB_after.setCheckable(False)
            self.cB_after.setEnabled(False)
            self.sB_hour.setEnabled(False)
            self.sB_minute.setEnabled(False)
            self.sB_second.setEnabled(False)
            self.hour_lab.setEnabled(False)
            self.min_lab.setEnabled(False)
            self.sec_lab.setEnabled(False)
        elif self.cB_timestamp.isChecked() == False:
            self.cB_after.setCheckable(True)
            self.cB_after.setEnabled(True)
            self.sB_hour.setEnabled(True)
            self.sB_minute.setEnabled(True)
            self.sB_second.setEnabled(True)
            self.hour_lab.setEnabled(True)
            self.min_lab.setEnabled(True)
            self.sec_lab.setEnabled(True)

    def createDateTime(self, q_dateTime):
        if (type(datetime.datetime.fromtimestamp(time.time())) == type(q_dateTime)):
            return q_dateTime
        return q_dateTime.dateTime().toPyDateTime()

    def intDateTime(self, q_dateTime):
        return int(self.createDateTime(q_dateTime).timestamp())


    def shutdown(self):
        self.lineE_option.setText("Shut down")
        self.lineE_seconds.setText(str(self.time))
        for i in range (1,self.time):
            self.lineE_seconds.setText(str(self.time-i))
            time.sleep(1)
            if self.stop:
                break
        print("Shut Down!")
        #if not self.stop:
        #   subprocess.call(["shutdown","/s"])

    def restart(self):
        self.lineE_option.setText("Restart")
        self.lineE_seconds.setText(str(self.time))
        for i in range (1,self.time):
            self.lineE_seconds.setText(str(self.time-i))
            time.sleep(1)
            if self.stop:
                break
        print("Restart!")
        #if not self.stop:
        #    subprocess.call(["shutdown", "/r"])

    def logout(self):
        self.lineE_option.setText("Logout")
        self.lineE_seconds.setText(str(self.time))
        for i in range (1,self.time):
            self.lineE_seconds.setText(str(self.time-i))
            time.sleep(1)
            if self.stop:
                break
        print("Logout!")
        #if not self.stop:
        #     subprocess.call(["shutdown", "/l"])

    def abort(self):
        try:
            subprocess.call(["shutdown", "/a"])
        except:
            pass
        self.stop = True
        self.lineE_option.setText("")
        self.lineE_seconds.setText("")
        self.lineE_option.setEnabled(False)
        self.lineE_seconds.setEnabled(False)
        self.pB_start.setEnabled(True)
        self.pB_abort.setEnabled(False)

    def newTask(self,target):
        task = Worker(target)
        task.setDaemon(True)
        task.start()

