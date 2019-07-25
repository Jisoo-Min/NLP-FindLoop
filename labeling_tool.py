import json
from pathlib import Path
import pandas as pd
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel,
                             QComboBox, QTextEdit, QLineEdit, QMessageBox)

class ToggleButton(QPushButton):
    def __init__(self, token, num, ID): # 문제번호, 인덱스
        self.ID = ID    # 토큰 인덱스
        self.num = num
        self.token = token
        QPushButton.__init__(self, token)
        #self.setFixedSize(40, 20)
        self.setStyleSheet("background-color: white")

        self.setCheckable(True)
        self.toggled.connect(self.slot_toggle)

    def slot_toggle(self, state):
        # toggle 상태에 따라 배경색 전환
        self.setStyleSheet("background-color: %s" % ({True: "red", False: "white"}[state]))
        # 레이블 변경
        ex.changeDataset(self.token, self.ID, state) # True를 받으면 P로 False를 받으면 I로 바꾸면 됨

class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 1                       # 문제 번호
        self.dbfilename = 'dataset.json'   # 데이터셋 파일명

        self.initUI()

        # 1. LOAD
        self.questions = [] # 코딩문제
        self.dataset = {}   # 레이블이 달린 데이터셋

        self.readDB()
        self.showDB()       # self.num에 해당하는 문제를 불러와서, 동적으로 버튼 생성.
        self.initDataset(); # (?) 문제 가능

    def initUI(self):
        # 1. Widget 생성
        # Label Widgets
        self.num_title = QLabel('#Q : ' + str(self.num))
        move_title = QLabel("Move to : ")


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


        # PushButton 에 함수 연결 (내가 정의한 함수)
        next_button.clicked.connect(self.buttonClicked)
        move_button.clicked.connect(self.buttonClicked)
        save_button.clicked.connect(self.buttonClicked)
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
        allbox.addLayout(box3)
        allbox.addLayout(self.box4)
        allbox.addLayout(box5)

        self.setLayout(allbox)

        self.setGeometry(600, 400, 500, 300)
        self.setWindowTitle('Label Tool')
        self.show()

    # 에러가 발생할때마다 메시지 창을 띄우는 메소드
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

    # write the data into db
    def writeDB(self):
        json.dump(self.dataset, open(f'dataset.json', 'w+'))

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

    # 현재 self.num에 해당하는 데이터를 불러와서, 동적 버튼 생성
    def showDB(self):
        # box4의 모든 위젯 삭제
        self.unfill()

        # box4에 새로운 위젯 추가 (1행당 10개 위젯)
        count = 0
        temp_h_box = QHBoxLayout() # 1행

        tokens = (self.questions[self.num]).split()

        i = 0
        for token in tokens:
            temp_h_box.addWidget(ToggleButton(token, self.num, i))
            count += 1
            i += 1
            if count == 10:
                self.box4.addLayout(temp_h_box)
                temp_h_box = QHBoxLayout()
                count = 0
        self.box4.addLayout(temp_h_box)

    # 1. 처음 시작 2. next, 3. move 버튼 누를떄 호출
    # 처음 접근한 문제인 경우, dataset의 해당 문제를 I 레이블로 초기화
    def initDataset(self):
        if str(self.num) not in self.dataset:
            tokens = (self.questions[self.num]).split()
            listOfTuples = []
            for token in tokens:
                listOfTuples.append((token, "I"))
            self.dataset[str(self.num)] = listOfTuples

    #self.changeDataset(self.ID, state)  # True를 받으면 P로 바꾸면 됨
    def changeDataset(self, token, ID, state):  # True를 받으면 P로 바꿈
        label = 'P' if state else 'I'
        self.dataset[str(self.num)][ID] = (token, label)

    def buttonClicked(self):
        sender = self.sender()
        button = sender.text() # 눌린 버튼의 이름

        if button == "Save":
            print('save')
            self.writeDB()

        else:
            if button == "Next":
                # Qnum 갱신
                self.num += 1
            if button == "Move":
                try:
                    a = self.questions[int(self.move_edit.text())]
                except:
                    self.msgBox("그지같은 입력 하지 마세연;")
                    return
                self.num = int(self.move_edit.text())

            self.num_title.setText('#Q : ' + str(self.num))
            self.initDataset();
            self.showDB();


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreDB()  # ScoreDB실행.
    sys.exit(app.exec_())