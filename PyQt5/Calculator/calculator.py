'''
calculator.py
Create a basic calculator application with BEDMAS and basic Add,Subtruct,Multi,Divide operators
Added Square Root, Memory and Squaring for Level 4
Added Music, Images and LCD Screen for 4+ 
'''
#imports
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QDesktopWidget,QGroupBox,QGridLayout,QFileDialog,QLCDNumber, QWidget,QLabel,QTextBrowser,QPushButton,QHBoxLayout,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtCore
import math

#Makes Class of QWidget
class Calculator(QWidget):
    #__init__ method 
    def __init__(self):
        #Runs method from parent class
        super(Calculator, self).__init__() 
        #Sets up the UI method
        self.initUI()
    
    def initUI(self):
        #X and Y Values for bliting buttons
        self.keyX = 0
        self.keyY = 100
        #Theres two values will be overrided so they don't matter
        self.XLocationOnScreen = 100
        self.YLocationOnScreen = 100
        #Size of widgets
        self.WidgetWidth = 270
        self.WidgetHeight = 550
        #Messages for the QLabels
        self.blankMessage = "---------Nothing was Inputted-----------"
        self.storeResultMessage = "Result was Stored"
        self.clearMemoryMessage = "Memory was Erased"
        self.fileNotFoundMessage = "Sorry, your file wasn't found"
        self.fileFullMessage = "Sorry, you file is too full"
        self.fileNoMemoryMessage = "Sorry, there is data in your Memory"
        self.undefinedMessage = "Undefined"
        
        #Creates QPushButtons with display and self
        #Numbers
        self.key1 = QPushButton('1',self)
        self.key2 = QPushButton('2',self)
        self.key3 = QPushButton('3',self)
        self.key4 = QPushButton('4',self)
        self.key5 = QPushButton('5',self)
        self.key6 = QPushButton('6',self)
        self.key7 = QPushButton('7',self)
        self.key8 = QPushButton('8',self)
        self.key9 = QPushButton('9',self)
        self.key0 = QPushButton('0',self)
        
        #Basic Opearators
        self.keyAddition = QPushButton('+',self)
        self.keySubtraction = QPushButton('-',self)
        self.keyMultiplication = QPushButton('*',self)
        self.keyDivision = QPushButton('/',self)
        #Squaring (Can only square one)
        #ie 5^2 = 25
        #5^2 + 3 = 28, not 3125
        self.keySquaring = QPushButton('^',self)
        #Can only do only squareRooting, no other operator besides decimal
        self.keySquareRooting = QPushButton('√',self)
        #Must be used at the beginning of the number and can't negative a negtaive number
        self.keyNegativeNumber = QPushButton('Negative ',self)
        self.keyDecimalPoint = QPushButton('Decimal ',self)
        #Enter key(Spacing for Spacing for button)
        self.keyEquals = QPushButton('    Enter   ',self)
        #Reset key to reset(doesn't touch memory)
        self.keyReset = QPushButton('  Reset   ',self)
        #Adds result to the memory
        self.keyStoreResult = QPushButton('Memory+',self)
        #Creates memory
        self.keyClearMemory = QPushButton('    M--    ',self)
        #retrrieves data from the memory
        self.keyRetrieveMemory = QPushButton('Memory-',self)
        #To open the music file
        self.keyOpenBtn = QPushButton('   Open   ',self)
        #Plays music file
        self.keyPlayBtn = QPushButton('   Play   ',self)
        
        #Creates QMediaPlayer for music      
        self.mediaPlayer = QMediaPlayer (None, QMediaPlayer.VideoSurface)
        #Creates LCD Screen to display result
        self.lcd = QLCDNumber(self)
        #Creates QLabel to display the text and inputs 
        self.outputScreen = QLabel(self.blankMessage,self)
        #Creates QPixmap to map out the pixels and sets path to the file
        self.calculatorImage = QPixmap("imageFiles/calculatorImage.png")
        #Creates Label to place the image file
        self.calculatorImageSlot = QLabel(self)
        #Sets up pixmap
        self.calculatorImageSlot.setPixmap(self.calculatorImage)


        #Array contenting all the different inputs
        self.outputScreenTextArray = []
        #String to display on the label
        self.outputScreenTextString = ""
        #The last input the user inputted
        self.lastInput = "None"
        #Latest number (To allow multiple digit numbers)
        self.latestNumber = ""
        #To allow only squaring if the user wants to use square rooting
        self.squareRootMode = False
        #The user can play the music without importing a file
        self.keyPlayBtn.setEnabled(False)

        #Display the lcd to start with 0 (needs an argument)
        self.lcd.display(0)
        #Sets up the maximum height
        self.lcd.setMaximumHeight(50)

        #Setup for the LCD Screen
        self.setObjectName("Dialog")
        #(60px left,0px down,moves 100 pixels left,80 pixels down)
        self.lcd.setGeometry(QtCore.QRect(10,10,250, 350))
        self.lcd.setObjectName("lcdNumber")
        self.translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self.translate("Dialog", "Dialog"))
        QtCore.QMetaObject.connectSlotsByName(self)

        #All the names for the keys for the small buttons 
        self.keyOrderSymbols = ['1','2','3','Addition','4','5','6','Subtraction','7','8','9','Multiplication','0','Squaring','SquareRooting','Division']
        #Names for larger buttons
        self.keyOrderWords = ['NegativeNumber','DecimalPoint','Equals','Reset','StoreResult','ClearMemory','RetrieveMemory','OpenBtn','PlayBtn']

        #Moves the keys 
        for key in self.keyOrderSymbols:
            #Moves keys using x and y values
            exec(f'self.key{key}.move(self.keyX,self.keyY)')
            #Moves buttons over
            self.keyX += 50
            #If the button has moved over, moves the button down and resets from the left
            if self.keyX == 200:
                self.keyY += 50
                self.keyX = 0

        for key in self.keyOrderWords:
            
            exec(f'self.key{key}.move(self.keyX,self.keyY)')
            self.keyX += 100

            if self.keyX == 200:
                self.keyY += 50
                self.keyX = 0
        #Moves the last two Slots without x and y
        self.calculatorImageSlot.move(200, 100)
        self.outputScreen.move(10,80)
        
        #self.
        #x,y,width,height (sets up width and height of the window and the x and y are overrided)
        self.setGeometry(self.XLocationOnScreen,self.YLocationOnScreen, self.WidgetWidth, self.WidgetHeight)
        
        #Centers the Window
        self.qtRectangle = self.frameGeometry()
        self.centerPoint = QDesktopWidget().availableGeometry().center()
        self.qtRectangle.moveCenter(self.centerPoint)
        self.move(self.qtRectangle.topLeft())
        
        #Links keys with methods and uses lambda to pass arguments
        self.key0.clicked.connect(lambda: self.numberPressed("0"))
        self.key1.clicked.connect(lambda: self.numberPressed("1"))
        self.key2.clicked.connect(lambda: self.numberPressed("2"))
        self.key3.clicked.connect(lambda: self.numberPressed("3"))
        self.key4.clicked.connect(lambda: self.numberPressed("4"))
        self.key5.clicked.connect(lambda: self.numberPressed("5"))
        self.key6.clicked.connect(lambda: self.numberPressed("6"))
        self.key7.clicked.connect(lambda: self.numberPressed("7"))
        self.key8.clicked.connect(lambda: self.numberPressed("8"))
        self.key9.clicked.connect(lambda: self.numberPressed("9"))

        self.keyAddition.clicked.connect(lambda: self.operatorPressed(" + "))
        self.keySubtraction.clicked.connect(lambda: self.operatorPressed(" - "))
        self.keyMultiplication.clicked.connect(lambda: self.operatorPressed(" * "))
        self.keyDivision.clicked.connect(lambda: self.operatorPressed(" / "))

        self.keySquaring.clicked.connect(lambda: self.operatorPressed(" ^ "))
        self.keySquareRooting.clicked.connect(self.squareRootPressed)
        self.keyNegativeNumber.clicked.connect(self.negativeNumberPressed)
        self.keyDecimalPoint.clicked.connect(self.decimalPointPressed)

        self.keyReset.clicked.connect(lambda: self.resetPressed(self.blankMessage))
        self.keyEquals.clicked.connect(self.equalsPressed)

        self.keyStoreResult.clicked.connect(self.storeResultInFile)
        self.keyClearMemory.clicked.connect(self.clearMemory)
        self.keyRetrieveMemory.clicked.connect(self.retrieveMemory)

        self.keyOpenBtn.clicked.connect(self.openFile)
        self.keyPlayBtn.clicked.connect(self.playMusic)

        #Sets up the name of the window
        self.setWindowTitle('Ishan Calculator Application')
        #displays widget
        self.show()

    #If the user clicked a number
    def numberPressed(self, numberValue):
        #Can't be inputted after clicking equals
        if self.lastInput != "Equals":
            #Adds the number value to the latest number
            self.latestNumber = self.latestNumber + numberValue
            #Adds the numberValue to the string and updates text
            self.outputScreenTextString = self.outputScreenTextString + numberValue
            self.outputScreen.setText(self.outputScreenTextString)
            #Sets up the last input to only allow certain inputs after 
            self.lastInput = "Number"
            
    #If the user clicked an operator
    def operatorPressed(self, operatorValue):
        #Only after certain inputs
        if self.lastInput == "Number" and self.squareRootMode == False and self.lastInput != "Equals":
            #adds values to the array for calculation later
            self.outputScreenTextArray.append(self.latestNumber)
            self.outputScreenTextArray.append(operatorValue)
            #Sets and updates text
            self.outputScreenTextString = self.outputScreenTextString + operatorValue
            self.outputScreen.setText(self.outputScreenTextString)
            #Updates the last input    
            self.lastInput = "Operator"
            #Resets the latest number
            self.latestNumber = ""

    #If the user wants to square root
    def squareRootPressed(self):
        if self.outputScreenTextString == "":
            self.outputScreenTextArray.append("√")

            self.outputScreenTextString = self.outputScreenTextString + "√"
            self.outputScreen.setText(self.outputScreenTextString)
                          
            self.lastInput = "squareRoot"
            #Opens variable to prevents other inputs
            self.squareRootMode = True
            
    #If the user wants negative number
    def negativeNumberPressed(self):
        if self.lastInput == "Operator" or self.lastInput == "None":
            if self.squareRootMode == False:
                #Negative is "-"
                #Minus is " - "
                self.outputScreenTextArray.append("-")
                self.outputScreenTextString = self.outputScreenTextString + "-"
                self.outputScreen.setText(self.outputScreenTextString)
                self.lastInput = "negativeSign"
    #If the user wants a decimal point
    def decimalPointPressed(self):
        if self.lastInput != "Equals":
            #Prevents multiple decimal point in a single number
            for slot in self.latestNumber:
                if slot == ".":
                    return None

                
            self.latestNumber = self.latestNumber + "."      
            self.outputScreenTextString = self.outputScreenTextString + "."
            self.outputScreen.setText(self.outputScreenTextString)
            self.lastInput = "decimalPoint"
            
    #If the user wants their result
    def equalsPressed(self):
        if self.lastInput == "Number":
            #Adds the last number the array
            self.outputScreenTextArray.append(self.latestNumber)
            #For Square rooting, just calcs it 
            if self.squareRootMode == True:

                self.outputScreenTextArray[0] = math.sqrt(float(self.outputScreenTextArray[1]))
                self.outputScreenTextArray.pop()
                
            else:
                #If the result hasn't been fully calculated,
                while len(self.outputScreenTextArray) != 1:
                    #Just keep calculating
                    self.calculateResult()
                    #If dividing by 0, just set the text and finish up
                    if self.outputScreenTextString == "Undefined":
                        self.outputScreen.setText(self.outputScreenTextString)
                        self.lastInput = "Equals"
                        return None
            #Adds the equal sign and the result
            self.outputScreenTextString = self.outputScreenTextString + " = " + str(self.outputScreenTextArray[0])
            self.outputScreen.setText(self.outputScreenTextString)

            self.lastInput = "Equals"
            #Updates LCD Screen (Only displays result
            self.updateLCD(float(self.outputScreenTextArray[0]))

    #To calculate one operation        
    def calculateResult(self):
        #Checks for the operator in order and calls different method
        for input in self.outputScreenTextArray:
            if input == "-":
                self.completeNegativeNumbers()
                #breaks/returns none to exit method
                return None

        for input in self.outputScreenTextArray:
            if input == " ^ ":
                self.completeExponents()
                return None

        for input in self.outputScreenTextArray:
             
            if input == " * " or input == " / ":
                self.completeMultiDivi()
                return None


        for input in self.outputScreenTextArray:
            if input == " + " or input == " - ":
                self.completeAddSubtract()
                return None
    
    #If the reset button is clicked        
    def resetPressed(self,message):
        #Resets all variables 
        self.outputScreenTextArray = []
        self.outputScreenTextString = ""
        self.outputScreen.setText(message)
        self.updateLCD(0)
        self.latestNumber = ""
        self.lastInput = "None"
        self.squareRootMode = False

    #To add the negative symbols to the numbers
    def completeNegativeNumbers(self):
        #variable to check each element in the array
        arrayIndex = 0
        
        for i in self.outputScreenTextArray:
            #If a negative symbol is found..
            if i == "-":
                #Calculate the result
                smallResult = -1 * float(self.outputScreenTextArray[arrayIndex + 1])

                #Remove the two elements ( "-" and 2)
                for i in range(2):
                    self.outputScreenTextArray.pop(arrayIndex)

                #adds "-2"
                self.outputScreenTextArray.insert(arrayIndex,smallResult)
                #return to exit the method
                return None
            #Moves the array index over one
            arrayIndex += 1
    #For decimal points
    def completeDecimalPoint(self):
        arrayIndex = 0
        
        for i in self.outputScreenTextArray:
            
            if i == "-":
                smallResult = -1 * float(self.outputScreenTextArray[arrayIndex + 1])

                
                for i in range(2):
                    self.outputScreenTextArray.pop(arrayIndex)


                self.outputScreenTextArray.insert(arrayIndex,smallResult)
                
                return None

            arrayIndex += 1
    #For exponents
    def completeExponents(self):
        arrayIndex = 0
        
        for i in self.outputScreenTextArray:
            
            if i == " ^ ":
                smallResult = float(self.outputScreenTextArray[arrayIndex - 1]) ** float(self.outputScreenTextArray[arrayIndex + 1])
                #Removes 3 elements (2^3 --> 8)
                for i in range(3):
                    self.outputScreenTextArray.pop(arrayIndex - 1)

                self.outputScreenTextArray.insert(arrayIndex - 1,smallResult)
                
                return None

            arrayIndex += 1


    #For multiplication
    def completeMultiDivi(self):
        arrayIndex = 0
        
        for i in self.outputScreenTextArray:
            
            if i == " * ":
                
                smallResult = float(self.outputScreenTextArray[arrayIndex - 1]) * float(self.outputScreenTextArray[arrayIndex + 1])
   
                for i in range(3):
                    self.outputScreenTextArray.pop(arrayIndex - 1)

                self.outputScreenTextArray.insert(arrayIndex - 1,smallResult)

                
                return None
        
            if i == " / ":
                #Checks if divising by 0 and returns early before causing errors
                if self.outputScreenTextArray[arrayIndex + 1] == "0":
                    self.outputScreenTextString = "Undefined"
                    return None
                
                smallResult = float(self.outputScreenTextArray[arrayIndex - 1]) / float(self.outputScreenTextArray[arrayIndex + 1])

    
                for i in range(3):
                    self.outputScreenTextArray.pop(arrayIndex - 1)

                self.outputScreenTextArray.insert(arrayIndex - 1,smallResult)

                return None

            arrayIndex += 1
    #For addition / subtraction
    def completeAddSubtract(self):
        arrayIndex = 0
        
        for i in self.outputScreenTextArray:

            if i == " + ":
                smallResult = float(self.outputScreenTextArray[arrayIndex - 1]) + float(self.outputScreenTextArray[arrayIndex + 1])

                for i in range(3):
                    self.outputScreenTextArray.pop(arrayIndex - 1)

                self.outputScreenTextArray.insert(arrayIndex - 1,smallResult)
                
                return None
        
            if i == " - ":
                smallResult = float(self.outputScreenTextArray[arrayIndex - 1]) - float(self.outputScreenTextArray[arrayIndex + 1])

                for i in range(3):
                    self.outputScreenTextArray.pop(arrayIndex - 1)

                self.outputScreenTextArray.insert(arrayIndex - 1,smallResult)

                return None    
        
            arrayIndex += 1
    #To update the lcd screen
    def updateLCD(self,result):
        #resets the lcd screen
        self.lcd.display(0)
        #Checks the length of the result to be displayed
        resultLength = len(str(result))
        #Sets the digitcount so all digits can be displayed
        self.lcd.setDigitCount(resultLength)

        #updates
        self.lcd.display(float(result))
    #To open the music file
    def openFile(self):
        #opens the fil manager and asks user for the file
        filename, _ = QFileDialog.getOpenFileName(self,"go Video")

        #If a file was found
        if filename != "":
            #Sets the file to be played for the path of the music file
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            #enables the play button
            self.keyPlayBtn.setEnabled(True)

    #To play the music 
    def playMusic(self):
        #Will pause the music if playing and playing if not playing 
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()
    #If the user wants to exit the program
    def closeEvent(self, event):
        #Asks the user if the program should quit
        quixBox = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if quixBox == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()

    def storeResultInFile(self):
        if self.lastInput == "Equals" and self.outputScreenTextString != "Undefined":
            #To see if there is data in the file
            fileDataArray = []
            #Attempts to open the file (read) and opens new loop
            try: 
                storageFile = open("calculatorFile.txt","r")
                openFile = True
            #If not, tell the user that the file isn't reachable
            except FileNotFoundError: 
                self.resetPressed(self.fileNotFoundMessage)
                
            #If successful...        
            if openFile:
                #For every line.....
                for line in storageFile: 
                    fileDataArray.append(str(line))
            
            #If the data file is empty
            if fileDataArray == []:
                #closes the file
                storageFile.close()
                #Opens with appending functionality
                storageFile = open("calculatorFile.txt","a")
                #write in the file and close
                storageFile.write(str(self.outputScreenTextArray[0]))
                #resets
                self.resetPressed(self.storeResultMessage)
                storageFile.close()
                
            else:
                self.resetPressed(self.fileFullMessage)

            
    #If the user wants to clear the memory in the file
    def clearMemory(self):
        #Opens the file and closes which erases contents 
        open('calculatorFile.txt', 'w').close()
        #resets
        self.resetPressed(self.clearMemoryMessage)

    #If the user wants to take data from the file
    def retrieveMemory(self):
        #array to store findings
        fileDataArray = []
                
        if self.lastInput != "Number" and self.lastInput != "Equals":
            #Trys opening the file after good inputs 
            try: 
                storageFile = open("calculatorFile.txt","r")
                openFile = True
            except FileNotFoundError: 
                self.resetPressed(self.fileNotFoundMessage)

            if openFile:
            #For every line.....
                for line in storageFile:
                    fileDataArray.append(str(line))

            #If data was found
            if fileDataArray != []:
                #adds data to the number pressed and closes file
                self.numberPressed(fileDataArray[0])

                storageFile.close()

            else:
                #Tells user that no data was found and closes file
                self.resetPressed(self.fileNoMemoryMessage)  
                storageFile.close()
                
        
def main():
    #Creates QApplication
    app = QApplication(sys.argv)
    #Creates class
    window = Calculator()
    sys.exit(app.exec_())

#Calls method
if __name__ == '__main__':
    main()
