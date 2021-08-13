#Ishan Phadte
#Allows the user to input a certain amount of questions for their test
#Allows them to provide a prompt and answer for the question
#Stores all data into 1 file

#imports
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import * 

#Class for Login Screen
class Login(QWidget):
    #To allow the use to switch windows
    switchWindow = QtCore.pyqtSignal()
    #Init method
    def __init__(self):
        #Runs parent class init
        QWidget.__init__(self)
        #Sets up Window Title
        self.setWindowTitle('Login')
        #Message for label(Big)
        self.enterMessage = "Welcome to the Ishan TestMaker 3000"
        #Sets up layout and location on computer
        basicWindowSetUp(self)
        #Centers Screen
        centerScreen(self)
        #Changes the background colour
        changeBackgroundColour(self,"Red")

        #Creates QPixmap to map out the pixels and sets path to the file
        self.loginImage = QPixmap("Images/loginImage.png")
        #Creates Label to place the image file
        self.loginImageSlot = QLabel(self)

        #Creates QLabel to display the text
        self.windowTextLabel = QLabel(self.enterMessage,self)
        #Creates QPushButton to move to next screen      
        self.keyLogin = QPushButton('Login')
        #Centers Label
        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        # setting font and size 
        self.windowTextLabel.setFont(QFont('Times', 30))     
        self.keyLogin.setFont(QFont('Times', 30))
        #If button is clicked, calls method
        self.keyLogin.clicked.connect(self.switchToQuestionAmountScreen)
        #Sets up pixmap
        self.loginImageSlot.setPixmap(self.loginImage)
        #Adds widget to layout
        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.loginImageSlot)
        self.layout.addWidget(self.keyLogin)
        #Sets up layout
        self.setLayout(self.layout)
    #If the button is clicked
    def switchToQuestionAmountScreen(self):
        #Clears the Test Storage File
        clearTest()
        #Moves to next screen
        self.switchWindow.emit()
#Class for asking for a desired amount of questions
class QuestionAmount(QWidget):

    switchWindow = QtCore.pyqtSignal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Question Amount Window')
        self.windowMessage = "Enter a number from 1 - 10 for the Number of Questions in the Test"


        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Red")

        self.questionAmountImage = QPixmap("Images/questionAmountImage.png")
        self.questionAmountImageSlot = QLabel(self)

        self.windowTextLabel = QLabel(self.windowMessage,self)
        #LineEdit allows uses to enter there own text 
        self.questionAmountUserInput = QLineEdit()
        self.keySwitchWindow = QPushButton('Switch Window')

        self.questionAmountImageSlot.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 30))     
        self.keySwitchWindow.clicked.connect(self.switchToQuestionTypeBuildingScreen)
        self.questionAmountImageSlot.setPixmap(self.questionAmountImage)


        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.questionAmountImageSlot)
        self.layout.addWidget(self.questionAmountUserInput)
        self.layout.addWidget(self.keySwitchWindow)


        self.setLayout(self.layout)

    def switchToQuestionTypeBuildingScreen(self):
        #Checks all numbers from 1-10 (Includes 1 and 10)
        for i in range(1,11):
            #If the input is a valid number
            if str(i) == self.questionAmountUserInput.text().strip():
                #Stores Data of the desried question amount in file
                storeDataInFile(str(self.questionAmountUserInput.text()))
                storeDataInFile(("\n"))
                storeDataInFile("^ Question(s) Desired")
                storeDataInFile(("\n"))
                storeDataInFile(("\n"))
                self.switchWindow.emit("")
#Class for Asking user which type of question they want to build
class QuestionTypeBuilding (QWidget):
    
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self,questionNumBuilding):
        QWidget.__init__(self)

        self.setWindowTitle('Question Type Window')
        self.windowMessage1 = "Which Type of Question would you Like to Build"
        #Will chnage based on the question being built
        self.windowMessage2 = "for Question " + str(questionNumBuilding) + "?"

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")

        self.windowTextLabel1 = QLabel(self.windowMessage1,self)
        self.windowTextLabel2 = QLabel(self.windowMessage2,self)

        self.questionTypeImage = QPixmap("Images/questionTypeImage.png")
        self.questionTypeImageSlot = QLabel(self)

        self.keyTF = QPushButton("True/False",self)
        self.keyMC = QPushButton("Mutliple Choice", self)
        self.keyFB = QPushButton("Fill in the Blank",self)

        self.windowTextLabel1.setAlignment(Qt.AlignCenter)
        self.windowTextLabel2.setAlignment(Qt.AlignCenter)
        self.questionTypeImageSlot.setAlignment(Qt.AlignCenter)

        self.windowTextLabel1.setFont(QFont('Times', 30))     
        self.windowTextLabel2.setFont(QFont('Times', 30))   
        #Lambda allowing button clicked to pass parameters
        self.keyTF.clicked.connect(lambda: self.switchToQuestionPromptBuildingScreen("TF"))
        self.keyMC.clicked.connect(lambda: self.switchToQuestionPromptBuildingScreen("MC"))
        self.keyFB.clicked.connect(lambda: self.switchToQuestionPromptBuildingScreen("FB"))
        self.questionTypeImageSlot.setPixmap(self.questionTypeImage)

        self.layout.addWidget(self.windowTextLabel1)
        self.layout.addWidget(self.windowTextLabel2)
        self.layout.addWidget(self.questionTypeImageSlot)
        self.layout.addWidget(self.keyTF)
        self.layout.addWidget(self.keyMC)
        self.layout.addWidget(self.keyFB)
  

        self.setLayout(self.layout)


    def switchToQuestionPromptBuildingScreen(self,questionType):
        storeDataInFile(str(int(readQuestionsFinished())+ 1)) 
        storeDataInFile("|")
        storeDataInFile(str(questionType) + "|")

        self.switchWindow.emit("")


#Class for building a Question Prompt
class QuestionPromptBuilding(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self,questionNumBuilding):
        QWidget.__init__(self)
        self.setWindowTitle('Question Prompt Window')
        self.windowMessage = "What Prompt for Question " + str(questionNumBuilding) + "?"


        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Blue")

        self.windowTextLabel = QLabel(self.windowMessage,self)
        self.questionPrompt = QLineEdit()
        self.keySwitchWindow = QPushButton('Switch Window')

        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 30))     
        self.keySwitchWindow.clicked.connect(self.switchToQuestionAnswerBuildingScreen)
        
        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.questionPrompt)
        self.layout.addWidget(self.keySwitchWindow)


        self.setLayout(self.layout)


    def switchToQuestionAnswerBuildingScreen(self):
        #If the Linedit isn't empty and no lineEdit errors were found
        if self.questionPrompt.text().strip() != "":
            if checkForTextErrors(self.questionPrompt.text().strip()) == False:
                storeDataInFile(str(self.questionPrompt.text().strip()) + "|")
                self.switchWindow.emit(" ")


#Class for building the answer for True/ False Questions 
class QuestionAnswerBuildingTrueFalse(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self,questionNumBuilding):
        QWidget.__init__(self)
        self.setWindowTitle('Question True/False Answer Window')
        self.windowMessage = "What is the Answer for Question " + str(questionNumBuilding) + "?"
        
        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Blue")

        self.windowTextLabel = QLabel(self.windowMessage,self)
        self.keyTrueCorrectAnswer = QPushButton('True')
        self.keyFalseCorrectAnswer = QPushButton('False')

        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 30))     

        self.keyTrueCorrectAnswer.clicked.connect(lambda: self.switchToNextScreen("True"))
        self.keyFalseCorrectAnswer.clicked.connect(lambda: self.switchToNextScreen("False"))

        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.keyTrueCorrectAnswer)
        self.layout.addWidget(self.keyFalseCorrectAnswer)


        self.setLayout(self.layout)

    def switchToNextScreen(self,correctAnswer):
        storeDataInFile(str(correctAnswer) + "|" + "*")
        storeDataInFile(("\n"))
        self.switchWindow.emit(" ")

#Class for building the answer for Multiple Choice Questions 
class QuestionAnswerBuildingMultipleChoice(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self,questionNumBuilding):
        QWidget.__init__(self)
        self.setWindowTitle('Question Multiple Choice Answer Window')
        self.windowMessage1 = "What is the Text Associated with the Different Responses?"
        self.windowMessage2 = "What is the Correct Answer for Question " + str(questionNumBuilding) + "?"

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Blue")

        self.windowTextLabel1 = QLabel(self.windowMessage1,self)
        self.windowTextLabel2 = QLabel(self.windowMessage2,self)
        self.keySwitchWindow = QPushButton('Done?')
        self.keyQuestionAnswerTextA = QLineEdit("TextA",self)
        self.keyQuestionAnswerTextB = QLineEdit("TextB",self)
        self.keyQuestionAnswerTextC = QLineEdit("TextC",self)
        self.keyQuestionAnswerTextD = QLineEdit("TextD",self)
        #Creates QCheckBox Objects 
        self.keyCheckBoxA = QCheckBox("A", self) 
        self.keyCheckBoxB = QCheckBox("B", self) 
        self.keyCheckBoxC = QCheckBox("C", self) 
        self.keyCheckBoxD = QCheckBox("D", self) 


        self.windowTextLabel1.setAlignment(Qt.AlignCenter)
        self.windowTextLabel1.setFont(QFont('Times', 20)) 
        self.windowTextLabel2.setAlignment(Qt.AlignCenter)
        self.windowTextLabel2.setFont(QFont('Times', 20))      
        self.keyCheckBoxA.setChecked(True) 
        # calling the uncheck method if any check box state is changed 
        self.keyCheckBoxA.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxB.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxC.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxD.stateChanged.connect(self.uncheck) 

        self.keySwitchWindow.clicked.connect(self.switchToNextScreen)

        self.layout.addWidget(self.windowTextLabel1)
        self.layout.addWidget(self.keyQuestionAnswerTextA)        
        self.layout.addWidget(self.keyQuestionAnswerTextB)        
        self.layout.addWidget(self.keyQuestionAnswerTextC)        
        self.layout.addWidget(self.keyQuestionAnswerTextD)
        self.layout.addWidget(self.windowTextLabel2)
        self.layout.addWidget(self.keyCheckBoxA)
        self.layout.addWidget(self.keyCheckBoxB)
        self.layout.addWidget(self.keyCheckBoxC)
        self.layout.addWidget(self.keyCheckBoxD)
        self.layout.addWidget(self.keySwitchWindow)

        self.setLayout(self.layout)

    def switchToNextScreen(self,correctAnswer):
        if self.keyQuestionAnswerTextA.text().strip() != "" and self.keyQuestionAnswerTextB.text().strip() != "" and self.keyQuestionAnswerTextC.text().strip() != "" and self.keyQuestionAnswerTextD.text().strip() != "":
        
            if checkForTextErrors(self.keyQuestionAnswerTextA.text().strip()) == False and checkForTextErrors(self.keyQuestionAnswerTextB.text().strip()) == False and checkForTextErrors(self.keyQuestionAnswerTextC.text().strip()) == False and checkForTextErrors(self.keyQuestionAnswerTextD.text().strip()) == False:
                      
                #If a checkBox is checked...
                if self.keyCheckBoxA.isChecked():
                    storeDataInFile(("A|"))

                elif self.keyCheckBoxB.isChecked():
                    storeDataInFile(("B|"))

                elif self.keyCheckBoxC.isChecked():
                    storeDataInFile(("C|"))

                elif self.keyCheckBoxD.isChecked():
                    storeDataInFile(("D|"))

                storeDataInFile(str(self.keyQuestionAnswerTextA.text()) + "|")
                storeDataInFile(str(self.keyQuestionAnswerTextB.text()) + "|")
                storeDataInFile(str(self.keyQuestionAnswerTextC.text()) + "|")
                storeDataInFile(str(self.keyQuestionAnswerTextD.text()) + "|" + "*")

                storeDataInFile(("\n"))
                self.switchWindow.emit(" ")   

    # uncheck method 
    def uncheck(self, state): 
  
        # checking if state is checked 
        if state == Qt.Checked: 
  
            # if first check box is selected 
            if self.sender() == self.keyCheckBoxA: 
  
                # making other check box to uncheck 
                self.keyCheckBoxB.setChecked(False) 
                self.keyCheckBoxC.setChecked(False) 
                self.keyCheckBoxD.setChecked(False)
  
            # if second check box is selected 
            elif self.sender() == self.keyCheckBoxB: 
  
                # making other check box to uncheck 
                self.keyCheckBoxA.setChecked(False) 
                self.keyCheckBoxC.setChecked(False) 
                self.keyCheckBoxD.setChecked(False) 

            # if third check box is selected 
            elif self.sender() == self.keyCheckBoxC: 
  
                # making other check box to uncheck 
                self.keyCheckBoxA.setChecked(False) 
                self.keyCheckBoxB.setChecked(False) 
                self.keyCheckBoxD.setChecked(False) 

            # if fourth check box is selected 
            elif self.sender() == self.keyCheckBoxD: 
  
                # making other check box to uncheck 
                self.keyCheckBoxA.setChecked(False) 
                self.keyCheckBoxB.setChecked(False) 
                self.keyCheckBoxC.setChecked(False) 

#Class for building answers for Fill in the Blank Questions 
class QuestionAnswerBuildingFillBlanks(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self,questionNumBuilding):
        QWidget.__init__(self)
        self.setWindowTitle('Question FitB Answer Window')
        self.windowMessage = "What is the Correct Answer for Question " + str(questionNumBuilding) + "?"
        
        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Blue")

        self.questionAnswerImage = QPixmap("Images/questionAnswerImage.png")
        self.questionAnswerImageSlot = QLabel(self)
        self.windowTextLabel = QLabel(self.windowMessage,self)
        self.questionAnswer = QLineEdit()
        self.keySwitchWindow = QPushButton('Switch Window')

        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 20)) 
        self.keySwitchWindow.clicked.connect(self.switchToNextScreen)
        self.questionAnswerImageSlot.setPixmap(self.questionAnswerImage)


        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.questionAnswerImageSlot)
        self.layout.addWidget(self.questionAnswer)
        self.layout.addWidget(self.keySwitchWindow)

        self.setLayout(self.layout)

    def switchToNextScreen(self):
        if self.questionAnswer.text().strip() != "":
            if checkForTextErrors(self.questionAnswer.text().strip()) == False:
                storeDataInFile(str(self.questionAnswer.text().strip()) + "|"+ "*")
                storeDataInFile(("\n"))
                self.switchWindow.emit(" ")

#Class for displaying the end screen
class EndScreen(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('End Screen')
        self.windowMessage = "You Have Finished Creating Your Test"

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")
        
        #Media Player for Movie
        self.mediaPlayer = QMediaPlayer (None, QMediaPlayer.VideoSurface)
        #Widget for Movie
        videoWidget = QVideoWidget()
        self.keyOpen = QPushButton('Open Video',self)
        self.keyPlay = QPushButton('Play Video',self)
        #Label for the Movie
        self.movieLabel = QLabel()
        self.windowTextLabel = QLabel(self.windowMessage,self)

        #If key is pressed, calls method
        self.keyOpen.clicked.connect(self.openFile)
        #Play key isn't enabled
        self.keyPlay.setEnabled(False)
        #Sets up the play button
        self.keyPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        #Calls method
        self.keyPlay.clicked.connect(self.playVideo)
        #Sets up the label
        self.movieLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 20))         

        #For movie clip layout
        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.keyOpen)
        hboxLayout.addWidget(self.keyPlay)
        hboxLayout.addWidget(self.windowTextLabel)
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videoWidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.movieLabel)
        self.setLayout(vboxLayout)
        #Media player output is placed in the video widget
        self.mediaPlayer.setVideoOutput(videoWidget)
        
        
    def closeEvent(self, event):
        #Asks the user if the program should quit
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()
    #To open the movie file
    def openFile(self):
        #Sets the path for the file
        filename, _ = QFileDialog.getOpenFileName(self,"Open Video")
        #If a path is found, enables the play button
        if filename != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

            self.keyPlay.setEnabled(True)
    #To play the movie
    def playVideo(self):
        #Pauses clip if the clip is playing 
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        #play clip is the clip isn't playing 
        else:
            self.mediaPlayer.play()

#Class to control which class is being displayed
class Controller:
    #init method 
    def __init__(self):
        pass
    
    #To show the login screen
    def showLoginScreen(self):
        #Creates instance of the login class
        self.login = Login()
        #If the switch window is enabled, calls next method)
        self.login.switchWindow.connect(self.showQuestionAmountScreen)
        #Displays the instance 
        self.login.show()
    #To show the question Amount screen 
    def showQuestionAmountScreen(self):
        #Which question is being built currently(while will passed around)
        self.questionNumBuilding = 0
        #Which question was built last
        self.lastQuestionType = "NA"
        self.questionAmount = QuestionAmount()
        #Calls next method with lambda (passes variables)
        self.questionAmount.switchWindow.connect(lambda: self.showQuestionTypeBuildingScreen(self.questionNumBuilding,self.lastQuestionType))
        #Closes previous instance and open new instance
        self.login.close()
        self.questionAmount.show()
    #To ask to user which type of question they want to built
    def showQuestionTypeBuildingScreen(self,questionNumBuilding,lastQuestionType):
        #Increments the question being built
        questionNumBuilding += 1
        #Passes in the arguments into the class when built
        self.questionTypeBuilding = QuestionTypeBuilding(questionNumBuilding)
        self.questionTypeBuilding.switchWindow.connect(lambda: self.showQuestionPromptBuildingScreen(questionNumBuilding))
        #Closes object depending on the previous screen
        if lastQuestionType == "NA":
            self.questionAmount.close()

        if lastQuestionType == "TF":
            self.questionTFAnswerBuilding.close()

        if lastQuestionType == "MC":
            self.questionMCAnswerBuilding.close()

        if lastQuestionType == "FB":
            self.questionFBAnswerBuilding.close()

        self.questionTypeBuilding.show()  
    #To allow the user to build a prompt for the question
    def showQuestionPromptBuildingScreen(self,questionNumBuilding):
        self.questionPromptBuilding = QuestionPromptBuilding(questionNumBuilding)
        
        #Will move to a different screen based on the type of the question)
        if readQuestionType(readQuestionsFinished()) == 'TF':
            self.questionPromptBuilding.switchWindow.connect(lambda: self.showQuestionAnswerBuildingTrueFalseScreen(questionNumBuilding))

        elif readQuestionType(readQuestionsFinished()) == 'MC':
            self.questionPromptBuilding.switchWindow.connect(lambda: self.showQuestionAnswerBuildingMultipleChoiceScreen(questionNumBuilding))

        elif readQuestionType(readQuestionsFinished()) == 'FB':
            self.questionPromptBuilding.switchWindow.connect(lambda: self.showQuestionAnswerBuildingFillBlanksScreen(questionNumBuilding))
        
        self.questionTypeBuilding.close()
        self.questionPromptBuilding.show() 

    #Allows user to make the answer for a True False questions 
    def showQuestionAnswerBuildingTrueFalseScreen(self,questionNumBuilding):

        self.questionTFAnswerBuilding = QuestionAnswerBuildingTrueFalse(questionNumBuilding)
        #Sets up a new last Question 
        self.lastQuestionType = "TF"

        #If on the last question, will move to the end screen, else, 
        #move back to the question type screen
        if readQuestionAmount() == readQuestionsFinished():
            self.questionTFAnswerBuilding.switchWindow.connect(lambda: self.showEndScreen(self.lastQuestionType))

        else:
            self.questionTFAnswerBuilding.switchWindow.connect(lambda: self.showQuestionTypeBuildingScreen(questionNumBuilding,self.lastQuestionType))
        
        self.questionPromptBuilding.close()
        self.questionTFAnswerBuilding.show()

    #Allows user to make the answer for a Multiple Choice questions 
    def showQuestionAnswerBuildingMultipleChoiceScreen(self,questionNumBuilding):

        self.questionMCAnswerBuilding = QuestionAnswerBuildingMultipleChoice(questionNumBuilding)
        self.lastQuestionType = "MC"

        if readQuestionAmount() == readQuestionsFinished():
            self.questionMCAnswerBuilding.switchWindow.connect(lambda: self.showEndScreen(self.lastQuestionType))

        else:
            self.questionMCAnswerBuilding.switchWindow.connect(lambda: self.showQuestionTypeBuildingScreen(questionNumBuilding,self.lastQuestionType))
        
        self.questionPromptBuilding.close()
        self.questionMCAnswerBuilding.show()    

    #Allows user to make the answer for a Fill in the Blanks questions 
    def showQuestionAnswerBuildingFillBlanksScreen(self,questionNumBuilding):

        self.questionFBAnswerBuilding = QuestionAnswerBuildingFillBlanks(questionNumBuilding)
        self.lastQuestionType = "FB"

        if readQuestionAmount() == readQuestionsFinished():
            self.questionFBAnswerBuilding.switchWindow.connect(lambda: self.showEndScreen(self.lastQuestionType))

        else:
            self.questionFBAnswerBuilding.switchWindow.connect(lambda: self.showQuestionTypeBuildingScreen(questionNumBuilding,self.lastQuestionType))
        
        self.questionPromptBuilding.close()
        self.questionFBAnswerBuilding.show()               

    #To display the End Screen
    def showEndScreen(self,lastQuestionType):
        #Closes previous instance
        if lastQuestionType == "TF":
            self.questionTFAnswerBuilding.close()

        if lastQuestionType == "MC":
            self.questionMCAnswerBuilding.close()

        if lastQuestionType == "FB":            
            self.questionFBAnswerBuilding.close()

        self.endScreen = EndScreen()
        self.endScreen.show()  

#Places window in the middle of the screen
def basicWindowSetUp(self):
    #Doesn't matter
    self.XLocationOnScreen = 100
    self.YLocationOnScreen = 100
    #Widget Width and Height
    self.WidgetWidth = 600
    self.WidgetHeight = 600

    #x,y,width,height (sets up width and height of the window and the x and y are overrided)
    self.setGeometry(self.XLocationOnScreen,self.YLocationOnScreen, self.WidgetWidth, self.WidgetHeight)
    #New layout
    self.layout = QGridLayout()

#Centers screen
def centerScreen(self):
    #Centers the Window
    self.qtRectangle = self.frameGeometry()
    self.centerPoint = QDesktopWidget().availableGeometry().center()
    self.qtRectangle.moveCenter(self.centerPoint)
    self.move(self.qtRectangle.topLeft())

#Changes the background colour
def changeBackgroundColour(self,colour):
    #Creates Pallette
    palette = self.palette()
    #Sets the colour based on the parameter passed
    #Can't pass directly, must pass through this if statement 
    if colour == "Red":
        palette.setColor(self.backgroundRole(), Qt.red)

    if colour == "Green":
        palette.setColor(self.backgroundRole(), Qt.green)

    if colour == "Blue":
        palette.setColor(self.backgroundRole(), Qt.blue)

    #Sets up the pallette
    self.setPalette(palette)

#Stores Data in the Test Storage File
def storeDataInFile(data):
    #Opens file as write 
    storageFile = open("DataFiles/TestStorageFile.txt","a")
    #Writes data in the file
    storageFile.write(str(data))
    #Closes file
    storageFile.close()

#Tells user the amount of desired questions 
def readQuestionAmount():
    #Opens file on line 1 
    storageFile = open("DataFiles/FPTTestStorageFile.txt","r")

    for line in storageFile:
        #Strips the /n at the end (for the new line)
        line = line.rstrip()
        #Places each word in the line in the array
        #This would be soley the number on line 1 
        #Converts to int from string
        questionAmount = int(line)
        return questionAmount

#Tells user the amount of questions finished
def readQuestionsFinished():

    questionsFinished = 0

    with open("DataFiles/TestStorageFile.txt","r") as f:
        #Skips first 3 lines 
        for i in range(3):
            f.readline()
        #For every line, increments 
        for line in f:
            questionsFinished += 1
    f.close()

    return questionsFinished

#Will return the question type for a question on a given line
def readQuestionType(questionNum):
    #All info for the line
    lineInfo = []
    #Data for each piece of info
    currentInfo = ""
    with open("DataFiles/TestStorageFile.txt","r") as f:
        #Ignores all lines before desired line
        for i in range(2 + questionNum):
            f.readline()
        #For every line 
        for line in f:
            #For every character in the line
            for character in line:
                #If the character isn't a divider
                if character != "|":
                    #Adds data to current info
                    currentInfo = currentInfo + character
                #If a divider was reached
                else:
                    #Adds the currentInfo the lineInfo
                    lineInfo.append(currentInfo)
                    #Refreshs the current Infor
                    currentInfo = ""
            #Closes the file and returns the second item(Type of question)
            f.close()
            return lineInfo[1]

#Returns True if an Error was found, 
#Returns False if no Errors were found (No Invalid inputs)
def checkForTextErrors(lineEdit):
    #For every character
    for character in lineEdit:
        #If an invalid character was found
        if character == "*" or character == "|":
            #return True
            return True
    #If nothing bad was found, returns False
    return False
    

#Clears the test
def clearTest():
    #Opens the file and closes which erases contents 
    open('DataFiles/TestStorageFile.txt', 'w').close()


#Setup
def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.showLoginScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
