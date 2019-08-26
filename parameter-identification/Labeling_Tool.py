import json
from pathlib import Path
import pandas as pd
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QTextEdit, QLineEdit, QMessageBox)

maxLabel = 5 # Maximum num of labels
minLabel = 1 # Default num of labels is 1 (label 'X')
colors = {'0': "white", '1': "red", '2': "orange", '3': "yellow", '4': 'green'}

# Button for each Label
class LabelButton(QPushButton):
    def __init__(self, Qnum, name, index): # Question_number, Label_name, Label_index(num)
        self.Qnum = Qnum
        if len(name) == 0 : name = "P"
        self.name = name
        self.index = index

        QPushButton.__init__(self, name)
        self.setStyleSheet("background-color: white; font : 30pt")
        self.setMaximumSize(300,50)

        self.setCheckable(False)
        self.clicked.connect(self.slot_toggle)
    def slot_toggle(self, state):
        #ex.showDB();
        pass

# Button for each Token
class ToggleButton(QPushButton):
    def __init__(self, token, Qnum, ID, label = '0'): #
        self.num = Qnum      # Question_number
        self.token = token  # token name
        self.ID = ID        # token index(num)
        self.label = label  # label

        QPushButton.__init__(self, token)
        self.setStyleSheet("background-color: white; font : 30pt")
        self.setCheckable(False)
        self.clicked.connect(self.slot_toggle)
    # Called when ToggleButton clicked
    def slot_toggle(self, state):
        # Change Button color based on status of button
        self.label = str((int(self.label) + 1) % ex.numOfLabel)
        self.setStyleSheet("background-color: %s; font : 30pt" % (colors[self.label]))

        # Change label of Button
        ex.changeDataset(self.token, self.ID, self.label)

class ScoreDB(QWidget):
    def __init__(self):
        super().__init__()
        self.num = 1                       # Question number

        # 둘다 페이지 바뀌면 1로 초기화.
        self.numOfLabel = minLabel         # 레이블 몇가지 종류?

        self.initUI()

        # 1. LOAD
        self.questions = [] # 코딩문제
        self.dataset = {}   # Labeled dataset     // {"1" : [(w1","0"), ("w2","1"), ..], [] }
        self.labelset = {}  # Label   set         // {"1" : ["label1", "label2"], "2" : ["label3"]}

        self.readDB()
        # Load Question(of which question number is self.num)
        # Generate all the button of that Question
        self.showDB()


    def initUI(self):
        # 1. Generating Widget
        # Label Widgets (Just Text)
        self.num_title = QLabel('Question ' + str(self.num))
        self.num_title.setStyleSheet("font : 25pt")

        move_title = QLabel("Move to : ")
        move_title.setStyleSheet("font : 25pt")

        self.numOfLabel_title = QLabel(str(self.numOfLabel - 1) + " labels : ")
        self.numOfLabel_title.setStyleSheet("font : 25pt")

        add_label_title = QLabel("Add Label : ")
        add_label_title.setStyleSheet("font : 25pt")

        check_title = QLabel('Check all the parameters : ')

        # Edit Widgets (Input Box)
        self.move_edit = QLineEdit()
        self.move_edit.setFixedSize(40,20)
        self.label_edit = QLineEdit()
        self.label_edit.setStyleSheet("font : 25pt")  # font

        # PushButton Widget (Button)
        next_button = QPushButton("Next")
        next_button.setStyleSheet("font : 25pt; background-color : gray; color : black")
        move_button = QPushButton("Move")
        save_button = QPushButton("Save")
        save_button.setStyleSheet("font : 25pt; background-color : gray; color : black")
        plus_button = QPushButton("+")
        plus_button.setStyleSheet("font : 25pt")
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("font : 25pt")


        # Connect function to PushButtons
        next_button.clicked.connect(self.buttonClicked)
        move_button.clicked.connect(self.buttonClicked)
        save_button.clicked.connect(self.buttonClicked)
        plus_button.clicked.connect(self.buttonClicked)
        reset_button.clicked.connect(self.buttonClicked)

        # 2. Layout

        # row 1 : box1
        box1 = QHBoxLayout()
        box1.addStretch(1)
        box1.addWidget(self.num_title)

        # row 2 : box2
        box2 = QHBoxLayout()
        box2.addStretch(1)
        box2.addWidget(move_title)
        box2.addWidget(self.move_edit)
        box2.addWidget(move_button)

        # row 3 : box2-1
        box2_1 = QHBoxLayout()
        box2_1.addStretch(1)
        box2_1.addWidget(self.numOfLabel_title)
        # 동적으로 레이블들을 보여줌
        self.boxOfLabels = QHBoxLayout()
        box2_1.addLayout(self.boxOfLabels)


        # row 4 : box2-2
        box2_2 = QHBoxLayout()
        box2_2.addStretch(1)
        box2_2.addWidget(add_label_title)
        box2_2.addWidget(self.label_edit)
        box2_2.addWidget(plus_button)
        box2_2.addWidget(reset_button)

        # row 5 : box3
        box3 = QHBoxLayout()
        box3.addStretch(1)
        box3.addWidget(check_title)

        # row 6 : box4
        # (Dynamically changed)
        self.box4 = QVBoxLayout()

        # row 7 : box5
        box5 = QHBoxLayout()
        box5.addWidget(save_button)
        box5.addWidget(next_button)


        # Main Layout(Vertical) : allbox
        allbox = QVBoxLayout()
        allbox.addStretch(1)
        allbox.addLayout(box1)
        allbox.addLayout(box2)
        allbox.addLayout(box2_1)
        allbox.addLayout(self.boxOfLabels)
        allbox.addLayout(box2_2)
        allbox.addLayout(box3)
        allbox.addLayout(self.box4)
        allbox.addLayout(box5)

        self.setLayout(allbox)

        self.setGeometry(600, 400, 500, 300)
        self.setWindowTitle('Label Tool')
        self.show()

    # Message Box for Exception
    def msgBox(self, message):
        reply = QMessageBox.question(self, 'Error!', message, QMessageBox.Yes, QMessageBox.Yes)

    # called when Window is closed
    def closeEvent(self, event):
        pass
        # self.writeDB()  # If we want, we can save current data when window is closed

    # load dataset and labelset
    def readDB(self):
        questions = pd.read_csv('Total_data_original - 시트1.csv')
        self.questions = questions["Original_Sentences"].tolist()

        try:
            self.dataset = json.loads(Path('dataset.json').read_text(), encoding='utf-8')
        except:
            self.dataset = {}
        try:
            self.labelset = json.loads(Path('labelset.json').read_text(), encoding='utf-8')
        except:
            self.labelset = {}

    # write the data into json file
    def writeDB(self):
        json.dump(self.dataset, open(f'dataset.json', 'w+'))
        json.dump(self.labelset, open(f'labelset.json', 'w+'))

    # Delete all the Widgets and Layouts of target
    def unfill(self, target):
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())
        deleteItems(target)

    # Update Page
    # 1. Load data of Question(of which question number is self.num)
    # 2. Delete current Widgets, Generate new Widgets
    def showDB(self):

        # =========== Initialization (if needed) ==========
        # If we access "self.num" at the first time, Initializing data for that number
        if str(self.num) not in self.dataset:
            self.initDataset(self.num)  # Initiate all the label as 'I' for "self.num" data

        # =========== Load ===========

        # 1. Load Tokens

        # 1-1. delete current TokenButtons
        self.unfill(self.box4)

        # 1-2. add new TokenButtons
        tokens = (self.questions[int(self.num)]).split()
        i = 0; count = 0;
        maxTokensOfRow = 10; # maximum tokens of each row is 10
        temp_h_box = QHBoxLayout()  # each row

        for token in tokens:
            label = self.dataset[str(self.num)][i][1]
            temp_button = ToggleButton(token, self.num, i, label)
            temp_button.setStyleSheet("background-color: %s; font : 30pt" % (colors[label]))

            temp_h_box.addWidget(temp_button)

            count += 1
            i += 1
            if count == maxTokensOfRow:
                self.box4.addLayout(temp_h_box)
                temp_h_box = QHBoxLayout()
                count = 0
        self.box4.addLayout(temp_h_box)

        # 2. Load Labels
        # 2-1. delete current LabelButtons
        self.unfill(self.boxOfLabels)
        # 2-2. add new LabelButtons
        temp_h_box = QHBoxLayout()
        labels = self.labelset[str(self.num)]
        for i in range(len(labels)):
            temp_button = LabelButton(self.num, labels[i], i)
            temp_button.setStyleSheet("background-color: %s; font : 30pt" % (colors[str(i+1)]))

            temp_h_box.addWidget(temp_button)
        self.boxOfLabels.addLayout(temp_h_box)

        # update "numOfLabel" and display it
        self.numOfLabel = len(labels) + 1
        self.numOfLabel_title.setText(str(len(labels)) + " labels")

    # Initiate all the label as 'I' for "self.num" data
    def initDataset(self, num):

        tokens = (self.questions[int(num)]).split()
        listOfTuples = []
        for token in tokens:
            listOfTuples.append((token, "0"))
        self.dataset[str(num)] = listOfTuples
        self.labelset[str(num)] = []
        self.numOfLabel = minLabel

        # Update numOfLabel
        self.numOfLabel_title.setText("No Label")

    # Change Label (for dataset)
    def changeDataset(self, token, ID, label): # token_name, question_num, label_name
        self.dataset[str(self.num)][ID] = (token, label)

    # Change Label (for labelset)
    def changeLabelset(self, num, label): # label_name
        if len(label) == 0: label = "P"
        self.labelset[str(self.num)].append(label)

    def buttonClicked(self):
        sender = self.sender()
        button = sender.text() # Name of Clicked Button
        targetNum = 0

        if button == "Save":
            self.writeDB()

        elif button == "+":
            if self.numOfLabel < maxLabel :
                label = self.label_edit.text()
                self.numOfLabel += 1
                self.label_edit.setText("")
                self.changeLabelset(self.num, label)
                self.showDB()
            else:
                self.msgBox("Too Many Labels")

            self.numOfLabel_title.setText(str(self.numOfLabel - 1) + " labels : ")

        elif button == "Reset":
            self.initDataset(self.num)
            self.showDB()
            pass
        else:
            if button == "Next":
                targetNum = int(self.num) + 1
            elif button == "Move":
                targetNum = self.move_edit.text()
                self.move_edit.setText("")
            # Check if Qnum is valid
            try:
                a = self.questions[int(targetNum)]
            except:
                self.msgBox("Invalid input")
                return

            # Update Question number
            self.num = targetNum
            self.num_title.setText('#Q : ' + str(self.num))

            # update page
            self.showDB();


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())
