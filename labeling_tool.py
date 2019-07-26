# 멀티레이블로 바꾸는중

import json
from pathlib import Path
import pandas as pd
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QTextEdit, QLineEdit, QMessageBox)
maxLabel = 5

class ToggleButton(QPushButton):
    def __init__(self, token, num, ID, label = '0'): # 문제번호, 인덱스
        self.num = num      # problem ID
        self.token = token  # token
        self.ID = ID        # token index
        self.label = label  # label

        QPushButton.__init__(self, token)
        self.setStyleSheet("background-color: white")
        #self.setStyleSheet("color: black")

        self.setCheckable(False)
        #self.toggled.connect(self.slot_toggle)
        self.clicked.connect(self.slot_toggle)
    def slot_toggle(self, state):
        # toggle 상태에 따라 배경색 전환
        # multi-label로 바꿔야함 (모듈로 사용) ============================ (수)
        #self.setFlat(False)

        self.label = str((int(self.label) + 1) % ex.numOfLabel)
        print("최대 레이블 개수 = ", ex.numOfLabel, "이 토큰의 label = ", self.label)

        self.setStyleSheet("background-color: %s" % (
            {'0': "white", '1': "red", '2' : "lime", '3' : "skyblue", '4' : 'purple' }[self.label])
                           )
        # ============================================================
        # 레이블 변경
        ex.changeDataset(self.token, self.ID, self.label)

class ScoreDB(QWidget):
    def __init__(self):
        super().__init__()
        self.num = 1                       # 문제 번호
        self.dbfilename = 'dataset.json'   # 데이터셋 파일명

        # 둘다 페이지 바뀌면 1로 초기화.
        self.numOfLabel = 2                # 레이블 몇가지 종류?

        self.initUI()

        # 1. LOAD
        self.questions = [] # 코딩문제
        self.dataset = {}   # 레이블이 달린 데이터셋

        self.readDB()
        self.showDB()       # self.num에 해당하는 문제를 불러와서, 동적으로 버튼 생성.

    def initUI(self):
        # 1. Widget 생성
        # Label Widgets
        self.num_title = QLabel('#Q : ' + str(self.num))
        move_title = QLabel("Move to : ")
        self.numOfLabel_title = QLabel("num of labels : " + str(self.numOfLabel))


        check_title = QLabel('Check all the parameters : ')

        # self. 를 붙여야 이 메소드가 끝나도 객체로부터 값을 읽어올 수 있음
        # Edit Widgets : 값 입력칸
        self.move_edit = QLineEdit()


        # # Text Widgets : 긴 값 입력칸
        # self.parameters_text = QTextEdit()

        # PushButton 생성
        next_button = QPushButton("Next")
        move_button = QPushButton("Move")
        save_button = QPushButton("Save")
        plus_button = QPushButton("+")
        minus_button = QPushButton("-")


        # PushButton 에 함수 연결 (내가 정의한 함수)
        next_button.clicked.connect(self.buttonClicked)
        move_button.clicked.connect(self.buttonClicked)
        save_button.clicked.connect(self.buttonClicked)
        plus_button.clicked.connect(self.buttonClicked)
        minus_button.clicked.connect(self.buttonClicked)
        # ----------------------------------------------

        # 2. Layout

        # 1행 : box1
        box1 = QHBoxLayout()
        box1.addStretch(1)
        box1.addWidget(self.num_title)

        # 2행 : box2
        box2 = QHBoxLayout()
        box2.addStretch(1)
        box2.addWidget(move_title)
        box2.addWidget(self.move_edit)
        box2.addWidget(move_button)

        # 2-2행 : box2-2
        box2_2 = QHBoxLayout()
        box2_2.addStretch(1)
        box2_2.addWidget(self.numOfLabel_title)
        box2_2.addWidget(plus_button)
        box2_2.addWidget(minus_button)


        # 3행 : box3
        box3 = QHBoxLayout()
        box3.addStretch(1)
        box3.addWidget(check_title)

        # 4행 : box4 (동적으로 바뀌어야함)
        self.box4 = QVBoxLayout()
        # ==여기에 동적으로 토글버튼 위젯들을 넣어야함==
        # for token in tokens:
        # ..

        # 5행 : box5
        box5 = QHBoxLayout()
        box5.addWidget(save_button)
        box5.addWidget(next_button)


        # allbox는 메인 레이아웃(세로박스)
        allbox = QVBoxLayout()
        allbox.addStretch(1)
        allbox.addLayout(box1)
        allbox.addLayout(box2)
        allbox.addLayout(box2_2)
        allbox.addLayout(box3)
        allbox.addLayout(self.box4)
        allbox.addLayout(box5)

        self.setLayout(allbox)

        self.setGeometry(600, 400, 500, 300)
        self.setWindowTitle('Label Tool')
        self.show()

    # 예외처리 용 메시지 박스
    def msgBox(self, message):
        reply = QMessageBox.question(self, '그지같은 입력 하지 마센;', message, QMessageBox.Yes, QMessageBox.Yes)

    def closeEvent(self, event):
        pass
        # self.writeDB()  # 창 끌 때 저장?

    def readDB(self):
        questions = pd.read_csv('Total_data_original - 시트1.csv')
        self.questions = questions["Original_Sentences"].tolist()

        try:
            self.dataset = json.loads(Path('dataset.json').read_text(), encoding='utf-8')
        except:
            self.dataset = {}

    # write the data into json file
    def writeDB(self):
        json.dump(self.dataset, open(f'dataset.json', 'w+'))

    # box4 의 모든 레이아웃, 위젯 삭제
    def unfill(self):
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())
        deleteItems(self.box4)

    # 현재 self.num에 해당하는 데이터를 불러와서, 버튼 생성
    def showDB(self):
        # box4의 모든 위젯 삭제
        print("showDB()")
        self.unfill()

        # box4에 새로운 위젯 추가 (1행당 10개 위젯)
        tokens = (self.questions[self.num]).split()
        i = 0  # 토큰 인덱스
        count = 0   # 1 ~ 10 카운트
        temp_h_box = QHBoxLayout()  # 1행

        if str(self.num) not in self.dataset:
            self.initDataset(self.num)  # 토큰의 모든 인덱스 'I'로 초기화.

        for token in tokens:
            label = self.dataset[str(self.num)][i][1]   # 토큰의 레이블
            temp_button = ToggleButton(token, self.num, i, label)
            temp_button.setStyleSheet("background-color: %s" % (
                {'0': "white", '1': "red", '2': "green", '3': "blue", '4': 'pink'}[label])
                               )
            temp_h_box.addWidget(temp_button)

            count += 1
            i += 1
            if count == 10:
                self.box4.addLayout(temp_h_box)
                temp_h_box = QHBoxLayout()
                count = 0
        self.box4.addLayout(temp_h_box)

    # 처음 접근한 문제인 경우, dataset의 해당 문제의 모든 token 레이블을 I 로 초기화.
    def initDataset(self, num): # num은 str으로 받아야함;;
        print("initDataset()")
        tokens = (self.questions[int(num)]).split()
        listOfTuples = []
        for token in tokens:
            listOfTuples.append((token, "0"))
        self.dataset[str(num)] = listOfTuples

    # 레이블을 변경
    def changeDataset(self, token, ID, label):
        self.dataset[str(self.num)][ID] = (token, label)

    def buttonClicked(self):
        sender = self.sender()
        button = sender.text() # 눌린 버튼의 이름
        targetNum = 0
        if button == "Save":
            self.writeDB()
        elif button == "+":
            if self.numOfLabel < maxLabel : self.numOfLabel += 1
            self.numOfLabel_title.setText("num of labels : " + str(self.numOfLabel))
        elif button == "-":
            if self.numOfLabel > 2: self.numOfLabel -= 1
            self.numOfLabel_title.setText("num of labels : " + str(self.numOfLabel))
        else:
            if button == "Next":
                targetNum = self.num + 1
            elif button == "Move":
                targetNum = int(self.move_edit.text())
            # 올바른 Qnum 인지 검사
            try:
                a = self.questions[targetNum]
            except:
                self.msgBox("불가능;;")
                return
            # == numOfLabel이 변경된 문제면 불러오고, 없으면 2로 초기화 해야함 ========= (당면 과제)


            # ==============================================================
            self.num = targetNum
            self.num_title.setText('#Q : ' + str(self.num))
            self.showDB();


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreDB()  # ScoreDB실행.
    sys.exit(app.exec_())
