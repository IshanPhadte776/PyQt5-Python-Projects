#Ishan Phadte
#FPTTestRunner.py
#February 2th 2021
#Allows user to enter their name,time and date
#Allows user to open the file containing the test and finish the test
#Will display the score and store all contains to the file
#Did all extras besides sending data through email
#Did movies and QCalenderWidget instead


#imports
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
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
        self.enterMessage = "Welcome to the Ishan TestTaker 3000"
        #Sets up layout and location on computer
        basicWindowSetUp(self)
        #Centers Screen
        centerScreen(self)
        #Changes the background colour
        changeBackgroundColour(self,"Red")


        #Creates QLabel to display the text
        self.windowTextLabel = QLabel(self.enterMessage,self)
        #Creates 
        self.nameLineEdit = QLineEdit("Insert Name Here",self)
        self.timeLineEdit = QLineEdit("Insert Time Here",self)
        #Creates QPixmap to map out the pixels and sets path to the file
        self.loginImage = QPixmap("Images/loginImage.png")
        #Creates Label to place the image file
        self.loginImageSlot = QLabel(self)
        self.keyLogin = QPushButton('Build and Start Test')

        #Sets up pixmap
        self.loginImageSlot.setPixmap(self.loginImage)
        self.keyLogin.clicked.connect(self.switchToNextScreen)

        #Centers Label
        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        # setting font and size 
        self.windowTextLabel.setFont(QFont('Times', 30))     
        #Adds objects to the lahyout 
        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.loginImageSlot)
        self.layout.addWidget(self.nameLineEdit)
        self.layout.addWidget(self.timeLineEdit)
        self.layout.addWidget(self.keyLogin)
        #Sets up the layout
        self.setLayout(self.layout)
    
    #When the button is clicked
    def switchToNextScreen(self):
        #If the line edit isn't empty  
        if self.nameLineEdit.text().strip() != "" and self.timeLineEdit.text().strip() != "" :
            #Clears the storage file(Ignores the file containing the test)
            clearExtraStorageFile()
            #Stores the name and new line in the file
            storeDataInFile(self.nameLineEdit.text().strip())
            storeDataInFile(("\n"))
            #Stores time too
            storeDataInFile(self.timeLineEdit.text().strip())
            storeDataInFile(("\n"))
            #Moves to the next screen
            self.switchWindow.emit()

#Calender Widget which allows the user to pick a date
class Calender(QWidget):

    switchWindow = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calender')

        basicWindowSetUp(self)
        centerScreen(self)

        #Creates VBoxLayout and CalenderWidget
        self.vbox = QVBoxLayout(self)
        self.Calender = QCalendarWidget(self)
        #Makes the grid visible
        self.Calender.setGridVisible(True)
        #Calls method if a date was selected
        self.Calender.clicked[QDate].connect(self.showDate)
        #Sets up the date
        self.date = self.Calender.selectedDate()
        #Adds objects to the layouts
        self.vbox.addWidget(self.Calender)
        self.setLayout(self.vbox)

        self.show()

    def showDate(self, date):
        #Stores data in file
        storeDataInFile(date.toString())
        storeDataInFile(("\n"))
        self.switchWindow.emit()

#Class for display text inbetween questions
class BetweenQuestions(QWidget):
    
    switchWindow = QtCore.pyqtSignal()
    #Passes in the question Num to accruate display text accordingly
    def __init__(self,questionNum):
        QWidget.__init__(self)

        self.setWindowTitle('Between Questions')

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")

        #Will display different text depending if the next question a real question or the test is done
        if questionNum > numOfQuestionsInTest():
            self.windowMessage = "Test is Finished, Continue to Result Screen?"
            
        else: 
            questionInfo = determineQuestionInfo(questionNum)
            self.windowMessage = "Ready for Question " + str(questionInfo[0]) + " ?"

        self.windowTextLabel = QLabel(self.windowMessage,self)

        self.keyNextScreen = QPushButton("Next Screen?")
        self.keyNextScreen.clicked.connect(self.switchToNextScreen)


        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.windowTextLabel.setFont(QFont('Times', 30))
  
        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.keyNextScreen)

        self.setLayout(self.layout)


    def switchToNextScreen(self):

        self.switchWindow.emit()

#Class to display True or False Questions 
class TrueFalseQuestion(QWidget):
    
    switchWindow = QtCore.pyqtSignal()

    def __init__(self,questionNum):
        QWidget.__init__(self)
        #Finds all the info for a certain question to be used for later 
        self.questionInfo = determineQuestionInfo(questionNum)
        self.setWindowTitle('True False Question')

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")

        self.questionPromptMessage = self.questionInfo[2]

        #Creates QLabel to display the text
        self.questionPromptLabel = QLabel(self.questionPromptMessage,self)


        self.keyTrue = QPushButton('True')
        self.keyFalse = QPushButton('False')

        self.keyTrue.clicked.connect(lambda: self.switchToNextScreen("True"))
        self.keyFalse.clicked.connect(lambda: self.switchToNextScreen("False"))

        self.questionPromptLabel.setAlignment(Qt.AlignCenter)
        self.questionPromptLabel.setFont(QFont('Times', 30))

        self.layout.addWidget(self.questionPromptLabel)
        self.layout.addWidget(self.keyTrue)
        self.layout.addWidget(self.keyFalse)

        self.setLayout(self.layout)


    def switchToNextScreen(self,input):
        #If the input is the same as data in the file(Correct Answer)
        if input == self.questionInfo[3]:
            #Stores, "Correct", else, stores Wrong 
            storeDataInFile("Correct")

        else:
            storeDataInFile("Wrong")

        storeDataInFile(("\n"))

        self.switchWindow.emit()

#Class to display Multiple Choice Questions 
class MultipleChoiceQuestion(QWidget):
    
    switchWindow = QtCore.pyqtSignal()

    def __init__(self,questionNum):
        QWidget.__init__(self)
        self.questionInfo = determineQuestionInfo(questionNum)
        self.setWindowTitle('Question Multiple Choice Answer Window')
        
        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")

        self.questionPromptMessage = self.questionInfo[2]


        self.questionPromptLabel = QLabel(self.questionPromptMessage,self)
        self.multipleChoiceImage = QPixmap("Images/multipleChoiceImage.png")
        self.multipleChoiceImageSlot = QLabel(self)

        #Sets up the check boxes using the question info
        self.keyCheckBoxA = QCheckBox(self.questionInfo[4], self) 
        self.keyCheckBoxB = QCheckBox(self.questionInfo[5], self) 
        self.keyCheckBoxC = QCheckBox(self.questionInfo[6], self) 
        self.keyCheckBoxD = QCheckBox(self.questionInfo[7], self) 

        self.keySwitchWindow = QPushButton('Done?')

        self.questionPromptLabel.setAlignment(Qt.AlignCenter)
        self.multipleChoiceImageSlot.setAlignment(Qt.AlignCenter)

        self.multipleChoiceImageSlot.setPixmap(self.multipleChoiceImage)

        self.questionPromptLabel.setFont(QFont('Times', 30))
        self.keyCheckBoxA.setFont(QFont('Times', 30))
        self.keyCheckBoxB.setFont(QFont('Times', 30))
        self.keyCheckBoxC.setFont(QFont('Times', 30))
        self.keyCheckBoxD.setFont(QFont('Times', 30))


        self.keyCheckBoxA.setChecked(True) 

        # calling the uncheck method if any check box state is changed 
        self.keyCheckBoxA.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxB.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxC.stateChanged.connect(self.uncheck) 
        self.keyCheckBoxD.stateChanged.connect(self.uncheck) 

        self.keySwitchWindow.clicked.connect(self.switchToNextScreen)

        self.layout.addWidget(self.questionPromptLabel)  
        self.layout.addWidget(self.multipleChoiceImageSlot)  
        self.layout.addWidget(self.keyCheckBoxA)
        self.layout.addWidget(self.keyCheckBoxB)
        self.layout.addWidget(self.keyCheckBoxC)
        self.layout.addWidget(self.keyCheckBoxD)
        self.layout.addWidget(self.keySwitchWindow)

        self.setLayout(self.layout)


    def switchToNextScreen(self):
        #If Data from the file matchs with the correct box being checked, prints accordingly
        if self.keyCheckBoxA.isChecked():
            if self.questionInfo[3] == "A":
                storeDataInFile("Correct")

            else:
                storeDataInFile("Wrong")
            

        if self.keyCheckBoxB.isChecked():
            if self.questionInfo[3] == "B":
                storeDataInFile("Correct")

            else:
                storeDataInFile("Wrong")

        if self.keyCheckBoxC.isChecked():
            if self.questionInfo[3] == "C":
                storeDataInFile("Correct")

            else:
                storeDataInFile("Wrong")
        
        
        if self.keyCheckBoxD.isChecked():
            if self.questionInfo[3] == "D":
                storeDataInFile("Correct")

            else:
                storeDataInFile("Wrong")
        
        storeDataInFile(("\n"))

        self.switchWindow.emit()   

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

#Class to display Fill in the Blanks Questions 
class FillBlanksQuestion(QWidget):

    switchWindow = QtCore.pyqtSignal()

    def __init__(self,questionNum):
        QWidget.__init__(self)
        self.questionInfo = determineQuestionInfo(questionNum)

        self.setWindowTitle('Fill in the Blanks Question')
        self.questionPromptMessage = self.questionInfo[2]

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Green")

        self.questionPromptLabel = QLabel(self.questionPromptMessage,self)
        self.fillBlanksImage = QPixmap("Images/fillBlanksImage.png")
        self.fillBlanksImageSlot = QLabel(self)
        self.questionAnswer = QLineEdit("Answer Here",self)
        self.keySubmit = QPushButton('Submit')

        self.keySubmit.clicked.connect(self.switchToNextScreen)
        self.questionPromptLabel.setFont(QFont('Times', 30))
        self.fillBlanksImageSlot.setAlignment(Qt.AlignCenter)
        self.questionPromptLabel.setAlignment(Qt.AlignCenter)
        self.fillBlanksImageSlot.setPixmap(self.fillBlanksImage)

        self.layout.addWidget(self.questionPromptLabel)
        self.layout.addWidget(self.fillBlanksImageSlot)
        self.layout.addWidget(self.questionAnswer)
        self.layout.addWidget(self.keySubmit)

        self.setLayout(self.layout)

    def switchToNextScreen(self):
        if self.questionAnswer.text().strip() != "":
            if self.questionAnswer.text().strip() == self.questionInfo[3]:
                storeDataInFile("Correct")

            else:
                storeDataInFile("Wrong")

            storeDataInFile(("\n"))

            self.switchWindow.emit()

#Class to display the End Screen
class EndScreen(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('End Screen')
        #Finds the score and displays it eventually
        self.scoreMessage = findScore()
        storeDataInFile("Score:" + self.scoreMessage)
        storeDataInFile(("\n"))

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Red")

        self.windowTextLabel = QLabel("You Score was",self)
        self.playerScoreLabel = QLabel(self.scoreMessage,self)
        self.fillBlanksImageSlot = QLabel(self)

        #If the user scored 75% or higher, will display a better image 
        if scoreAboveOrEqual75() == True:
            self.fillBlanksImage = QPixmap("Images/homerGood.png")
        else:
            self.fillBlanksImage = QPixmap("Images/homerBad.png")

        self.windowTextLabel.setFont(QFont('Times', 30))
        self.playerScoreLabel.setFont(QFont('Times', 30))
        self.windowTextLabel.setAlignment(Qt.AlignCenter)
        self.playerScoreLabel.setAlignment(Qt.AlignCenter)
        self.fillBlanksImageSlot.setAlignment(Qt.AlignCenter)


        self.fillBlanksImageSlot.setPixmap(self.fillBlanksImage)

        self.layout.addWidget(self.windowTextLabel)
        self.layout.addWidget(self.playerScoreLabel)
        self.layout.addWidget(self.fillBlanksImageSlot)

        self.setLayout(self.layout)
    #If the user quits the window, asks if they really want to
    def closeEvent(self, event):
        #Asks the user if the program should quit
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()

#Class to tell user that the test file is empty and prevents errors
class ErrorScreen(QWidget):
    switchWindow = QtCore.pyqtSignal(str)   

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Error Screen')
        self.windowMessage1 = "It seems that the Test File was Empty"
        self.windowMessage2 = "Run the Test Creator Program first"

        basicWindowSetUp(self)
        centerScreen(self)
        changeBackgroundColour(self,"Red")

        self.windowTextLabel1 = QLabel(self.windowMessage1,self)
        self.windowTextLabel2 = QLabel(self.windowMessage2,self)
        self.homerBadImageSlot = QLabel(self)
        self.homerBadImage = QPixmap("Images/homerBad.png")


        self.windowTextLabel1.setFont(QFont('Times', 30))
        self.windowTextLabel2.setFont(QFont('Times', 30))
        self.windowTextLabel1.setAlignment(Qt.AlignCenter)
        self.windowTextLabel2.setAlignment(Qt.AlignCenter)
        self.homerBadImageSlot.setAlignment(Qt.AlignCenter)


        self.homerBadImageSlot.setPixmap(self.homerBadImage)

        self.layout.addWidget(self.windowTextLabel1)
        self.layout.addWidget(self.windowTextLabel2)
        self.layout.addWidget(self.homerBadImageSlot)

        self.setLayout(self.layout)



#Class to control other classes
class Controller:
    #Ignoes __init method
    def __init__(self):
        pass
    
    #To show the login screen
    def showLoginScreen(self):
        #Creates instance of the class
        self.login = Login()
        #One button click, calls method
        if checkForEmptyTestFile() == True:
            self.login.switchWindow.connect(self.showErrorScreen)

        else:
            self.login.switchWindow.connect(self.showCalenderScreen)
        #Shows instance of the class
        self.login.show()

    #Shows Calender Screen
    def showCalenderScreen(self):
        #Sets up variables to be passed 
        self.questionNum = 0
        self.lastQuestionType = "NA"
        self.calender = Calender()
        #Provides arguments to pass to method
        self.calender.switchWindow.connect(lambda: self.showBetweenQuestionScreen(self.questionNum,self.lastQuestionType))
        self.login.close()
        self.calender.show()


    def showBetweenQuestionScreen(self,questionNum,lastQuestionType):
        #Increments variable to go to next line in file
        questionNum += 1
        self.betweenQuestions = BetweenQuestions(questionNum)
        #Closes different instance depending on the Last Question Type
        if lastQuestionType == "NA":
            self.calender.close()

        elif lastQuestionType == "TF":
            self.questionTrueFalse.close()

        elif lastQuestionType == "MC":
            self.questionMultipleChoice.close()

        elif lastQuestionType == "FB":
            self.questionFillBlanks.close()

        #Will move to the end screen if the test is "Done" with questions 
        if questionNum > numOfQuestionsInTest():
            self.betweenQuestions.switchWindow.connect(self.showEndScreen)

        #If the question Type for a certain question is a certain string, calls different method
        elif readQuestionType(questionNum) == "TF":
            self.betweenQuestions.switchWindow.connect(lambda: self.showTrueFalseQuestion(questionNum))

        elif readQuestionType(questionNum) == "MC":
            self.betweenQuestions.switchWindow.connect(lambda: self.showMultipleChoiceQuestion(questionNum))

        elif readQuestionType(questionNum) == "FB":
            self.betweenQuestions.switchWindow.connect(lambda: self.showFillBlanksQuestion(questionNum))
                
        self.betweenQuestions.show()
    
    #If the type is a True False Question
    def showTrueFalseQuestion(self,questionNum):
        #Creates need variable to be passed
        self.lastQuestionType = "TF"
        self.questionTrueFalse = TrueFalseQuestion(questionNum)
        self.questionTrueFalse.switchWindow.connect(lambda:self.showBetweenQuestionScreen(questionNum,self.lastQuestionType))
        self.betweenQuestions.close()
        self.questionTrueFalse.show()

    #If the type is a Multiple Choice Question
    def showMultipleChoiceQuestion(self,questionNum):
        self.lastQuestionType = "MC"
        self.questionMultipleChoice = MultipleChoiceQuestion(questionNum)
        self.questionMultipleChoice.switchWindow.connect(lambda:self.showBetweenQuestionScreen(questionNum,self.lastQuestionType))
        self.betweenQuestions.close()
        self.questionMultipleChoice.show()

    #If the type of Fill in the Blanks
    def showFillBlanksQuestion(self,questionNum):
        self.lastQuestionType = "FB"
        self.questionFillBlanks = FillBlanksQuestion(questionNum)   
        self.questionFillBlanks.switchWindow.connect(lambda:self.showBetweenQuestionScreen(questionNum,self.lastQuestionType))
        self.betweenQuestions.close()
        self.questionFillBlanks.show()
    
    #To diplay the End Screen
    def showEndScreen(self):
        self.endScreen = EndScreen()
        self.betweenQuestions.close()
        self.endScreen.show()     

    #To display the Error Screen:
    def showErrorScreen(self):
        self.errorScreen = ErrorScreen()
        self.login.close()
        self.errorScreen.show()           


#To set up basic window
def basicWindowSetUp(self):
    self.XLocationOnScreen = 100
    self.YLocationOnScreen = 100
    self.WidgetWidth = 600
    self.WidgetHeight = 600

    #x,y,width,height (sets up width and height of the window and the x and y are overrided)
    self.setGeometry(self.XLocationOnScreen,self.YLocationOnScreen, self.WidgetWidth, self.WidgetHeight)

    self.layout = QGridLayout()

#To center the screen
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

    #Sets up the palette
    self.setPalette(palette)

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

#Same as above but returns all data, not just the questionType
def determineQuestionInfo(questionNum):

    lineInfo = []
    currentInfo = ""
    with open("DataFiles/TestStorageFile.txt","r") as f:
        for i in range(2 + questionNum):
            f.readline()
        for line in f:
            for character in line:
                if character != "|":
                    currentInfo = currentInfo + character

                else:
                    lineInfo.append(currentInfo)
                    currentInfo = ""

            f.close()
            return lineInfo
#Method to find the Score for all the answers
def findScore():
    #Variable to store all correct answers
    correctAnswers = 0
    #Variable to store all answers
    answers = 0
    #String to return
    score = ""

    with open("DataFiles/DataStorageFile.txt","r") as f:
        #Skips first 3 lines (Date and Name and Time)
        for i in range(3):
            f.readline()
        for line in f:
            line = line.rstrip()
            #If the line says "Correct"
            if line == "Correct":
                #Provides an extra correct answer
                correctAnswers += 1
            #Will increment answer for every line
            answers += 1
    #Develops string to be returned
    score = str(correctAnswers) + " / " + str(answers)

    return score

#Same as above method, but will return True if the score is above or equal 75%
def scoreAboveOrEqual75():
    correctAnswers = 0
    answers = -1
    score = 0

    with open("DataFiles/DataStorageFile.txt","r") as f:

        for i in range(3):
            f.readline()

        for line in f:
            line = line.rstrip()
            if line == "Correct":
                correctAnswers += 1
            
            answers += 1

    #Turns the score into a decimal
    score = correctAnswers / answers
    #Returns different value based on value of score
    if score >= 0.75:
        return True

    else:
        return False

#Will return the amount of questions in the test
def numOfQuestionsInTest():

    numOfQuestions = 0

    with open("DataFiles/TestStorageFile.txt","r") as f:
        for i in range(3):
            f.readline()
        for line in f:
            numOfQuestions += 1
    f.close()

    return numOfQuestions

#Will store data in the file 
def storeDataInFile(data):
    storageFile = open("DataFiles/DataStorageFile.txt","a")
    storageFile.write(str(data))
    storageFile.close()

#Clears extra data file
def clearExtraStorageFile():
    #Opens the file and closes which erases contents 
    open('DataFiles/DataStorageFile.txt', 'w').close()

#Checks if the test storage file is empty (To prevent errors)
#Returns True if we have an empty file
def checkForEmptyTestFile():
    testFile = open("DataFiles/TestStorageFile.txt","r")

    for line in testFile:
        return False

    return True


#Sets up program
def main():
    app = QApplication(sys.argv)
    controller = Controller()
    #Calls method in the class
    controller.showLoginScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


