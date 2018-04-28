""" G r a p h i c a l   U s e r   I n t e r f a c e """
import base64
import sys
import email.message as em
import BL
from PyQt4 import QtGui,QtCore 
""""""""""""""""""

class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textUser = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password) # hide text

        self.textUser.setPlaceholderText("Enter Your Email Here")
        self.textPass.setPlaceholderText("Enter Password Here")

        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.checkLogin)
        self.setWindowTitle("Login")

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textUser)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        self.setFixedSize(200,100)
        
    def checkLogin(self):
#        """DEBUG AUTO-LOGIN"""
#        if(BL.loginAuth(BL.EMAIL_ACCOUNT,BL.decode_password())[0]):
#            self.accept()
        
        BL.EMAIL_ACCOUNT = self.textUser.text()            
        BL.EMAIL_PASSWORD = self.textPass.text()

        if(BL.loginAuth(BL.EMAIL_ACCOUNT,BL.EMAIL_PASSWORD)):
            self.accept()           
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Wrong user or password')
    
class NewMail(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(NewMail, self).__init__(parent)
        self.initTextBoxes()
        self.initButtons()
        self.initTitles()
        
        self.setWindowTitle("New Mail")
        self.setFixedSize(500,400)

    def initTitles(self):
        self.titleNewMail = QtGui.QLabel(self)
        self.titleNewMail.setGeometry(0,0,500,50)
        self.titleNewMail.setAlignment(QtCore.Qt.AlignCenter)
        self.titleNewMail.setText("N E W   M E S S A G E") 
        
        self.titleTo = QtGui.QLabel(self)
        self.titleTo.move(0,50)
        self.titleTo.setText("  To:") 
        
        self.titleCC = QtGui.QLabel(self)
        self.titleCC.move(0,80)
        self.titleCC.setText("  CC:") 
        
        self.titleSubject = QtGui.QLabel(self)
        self.titleSubject.move(0,110)
        self.titleSubject.setText("  Subject:") 
        
    def initTextBoxes(self):                
        self.messageTo = QtGui.QLineEdit(self)
        self.messageTo.setGeometry(30,60,470,20)
        
        self.messageCC = QtGui.QLineEdit(self)
        self.messageCC.setGeometry(30,90,470,20)
        
        self.messageSubject = QtGui.QLineEdit(self)
        self.messageSubject.setGeometry(50,120,450,20)

        self.messageBody = QtGui.QTextEdit(self)
        self.messageBody.setGeometry(0,150,500,200)  
        
    def initButtons(self):

        self.btnSend = QtGui.QPushButton('Send', self)
        self.btnSend.move(0,350)
        self.btnSend.clicked.connect(self.sendButton)

        self.btnDiscard = QtGui.QPushButton('Clear', self)
        self.btnDiscard.move(100,350)
        self.btnDiscard.clicked.connect(self.clearFields)
                
    def sendButton(self):
        recipient = self.messageTo.text()        
        cc = self.messageCC.text()
        subject = self.messageSubject.text()
        message = self.messageBody.toPlainText()  # messageBody.toHtml()
    
    #        #self sending        
    #        BL.sendEmail("debug","",BL.EMAIL_ACCOUNT,BL.EMAIL_ACCOUNT)
    #        #debug data        
    #        print( 'From:' + BL.EMAIL_ACCOUNT + '\n' + 'To:  ' + recipient + '\n' + 'Subject:'+ subject + ' \n' + message + '\n')
    
        if(BL.sendEmail(subject,message,BL.EMAIL_ACCOUNT,recipient,cc)):
            QtGui.QMessageBox.information(self, 'Success', 'Email sent!')
        else:
            QtGui.QMessageBox.warning(self, 'Error', 
            'Sending failed! \nInvalid recipients or lost internet connection.')
        
        self.clearFields()
        
    def clearFields(self):
        self.messageSubject.setText("")
        self.messageBody.setText("") 
        self.messageCC.setText("") 
        self.messageTo.setText("") 
        
        
#//////////////////////////////////////////////////////////////////////////////            
# M A I N//////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////    
class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.initUI()
        self.refreshInboxList()
        
        self.newMail = NewMail(self)

    def initUI(self):
        self.initTextBoxesTitles()
        self.initTextBoxes()
        self.initButtons()
        
        self.startInboxList()
    
        self.setFixedSize(700,400)
        self.setWindowTitle("LAB_4 PR")

#//////////////////////////////////////////////////////////////////////////////            
# Q T   G U I   I N I T S /////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////    
  
    def initTextBoxes(self):                
        self.messageBody = QtGui.QTextEdit(self)
        self.messageBody.setGeometry(200,50,500,300)         

    def initTextBoxesTitles(self):                
        self.titleTo = QtGui.QLabel(self)
        self.titleTo.move(200,50)
        self.titleTo.setText("  To:") 
        
        self.titleCC = QtGui.QLabel(self)
        self.titleCC.move(200,80)
        self.titleCC.setText("  CC:") 
        
        self.titleSubject = QtGui.QLabel(self)
        self.titleSubject.move(200,110)
        self.titleSubject.setText("  Subject:") 
        
        self.textPageNr = QtGui.QLabel(self)
        self.textPageNr.setGeometry(30,350,30,30)
        self.textPageNr.setAlignment(QtCore.Qt.AlignCenter)
        self.textPageNr.setText("1")
        
        self.inboxTitle = QtGui.QLabel(self)
        self.inboxTitle.move(0,20)
        
        self.titleApp = QtGui.QLabel(self)
        self.titleApp.setGeometry(0,0,700,30)
        self.titleApp.setAlignment(QtCore.Qt.AlignCenter)
        self.titleApp.setText("E M A I L   C L I E N T   O N   S M T P  &  I M A P") 
        
    def initButtons(self):
        self.btnNew = QtGui.QPushButton('New', self)
        self.btnNew.move(200,350)        
        self.btnNew.clicked.connect(self.StartNewMail)#new window./////////////

#        self.btnDelete = QtGui.QPushButton('Delete', self)
#        self.btnDelete.move(300,20)

        self.btnHTML = QtGui.QPushButton('View as html', self)
        self.btnHTML.setGeometry(400,350,300,30)        
        self.btnHTML.clicked.connect(self.viewHTML)
        
        self.btnInboxBack = QtGui.QPushButton('<', self)
        self.btnInboxBack.setGeometry(0,350,30,30)        
        self.btnInboxBack.clicked.connect(self.inboxBack)

        self.btnInboxNext = QtGui.QPushButton('>', self)
        self.btnInboxNext.setGeometry(60,350,30,30)        
        self.btnInboxNext.clicked.connect(self.inboxNext)
        
        self.btnRefresh = QtGui.QPushButton('Refresh', self)
        self.btnRefresh.setGeometry(100,350,100,30)        
        self.btnRefresh.clicked.connect(self.refreshInboxList)
                
        
#    def initMenubar(self):        
#        eh, who needs this?
#
#        menubar = self.menuBar()        
#
#        mUser = menubar.addMenu("User")
#        mmchange = mUser.addAction("Change User")        
#        mmlogout = mUser.addAction("Log Out")        
#        
#        file = menubar.addMenu("File")
#        file_exit = file.addAction("Exit")
#        
#        edit = menubar.addMenu("Edit")
#        edit_undo = edit.addAction("Undo")
#        edit_redo = edit.addAction("Redo")         
#        edit_cut = edit.addAction("Cut")
#        edit_copy = edit.addAction("Copy")
#        edit_paste = edit.addAction("Paste")
#    
#        view = menubar.addMenu("View")
        

#//////////////////////////////////////////////////////////////////////////////            
# B U T T O N S ///////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////    

    def StartNewMail(self):
        self.newMail.show()
        
    def viewHTML(self):
        QtGui.QMessageBox.information(self, 'LOL', 'Not implemented!')
    
    def showMessage(self):
        num = self.listWidget.currentRow()
        body = BL.readEmail(self.inboxPage * self.mailsPerPage + num)
        self.fillFields(body)
        
    def fillFields(self,body):
        try:
            self.messageBody.setText(body)  
        except:
            self.messageBody.setText("Error Loading The Email / Unknown format")
            
    def startInboxList(self):
        self.unread = 0
        self.inboxPage = 0
        self.mailsPerPage = 4
    
        M,mail,self.unread = BL.showMail(self.inboxPage,self.mailsPerPage)
        self.inboxTitle.setText("  Inbox (" + str(self.unread) + ")") 
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setGeometry(0,50,200,300)
        self.listWidget.itemClicked.connect(self.showMessage)
        
        for i in range(self.mailsPerPage):
            item = QtGui.QListWidgetItem("Email preview %i" % i)
            self.listWidget.addItem(item) 
                
    def refreshInboxList(self):
        self.listWidget.clear()
        M,mail,self.unread = BL.showMail(self.inboxPage,self.mailsPerPage)
        self.inboxTitle.setText("  Inbox (" + str(self.unread) + ")") 
        
        try:
            for i in range(self.mailsPerPage):
                item = \
                    QtGui.QListWidgetItem(" From: {0}\
                                         \n Subject: {1}\
                                         \n Date: {2}\
                                         \n___________________________________"\
                .format(mail["from"][i].replace("\n"," "),
                        mail["subject"][i].replace("\n"," "), 
                        mail["date"][i].replace("\n"," ")))            
                self.listWidget.addItem(item)
                
        except:
            item = QtGui.QListWidgetItem(" \nNo more!\n")            
            self.listWidget.addItem(item)
            
            #todo: add if unseen, add widget box to capture atention
        
    def inboxNext(self):
        self.inboxPage+=1
        self.refreshInboxList()
        self.textPageNr.setText(str(self.inboxPage+1))
        
    def inboxBack(self):
        if self.inboxPage > 0:            
            self.inboxPage-=1
            self.refreshInboxList()
            self.textPageNr.setText(str(self.inboxPage+1))


#//////////////////////////////////////////////////////////////////////////////            
# M A I N ///// ///////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////    

def main():
    app = QtGui.QApplication(sys.argv)
    
    login = Login()
    if login.exec_() == QtGui.QDialog.Accepted:
        main = Main()
        main.show()
        sys.exit(app.exec_()) #close app
        
if __name__ == "__main__":
    main()
