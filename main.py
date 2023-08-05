from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
from datetime import datetime
import sys
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("starter")


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.course = None
        self.grid_layout = None
        self.weights = None
        self.button_close = None
        self.button_calculate = None
        self.result_label = None
        self.button_create = None
        self.row_input = None
        self.layout = None
        self.inputs = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("均分计算")
        self.layout = QVBoxLayout()

        self.row_input = QLineEdit()
        self.layout.addWidget(self.row_input)

        self.button_create = QPushButton("创建科目")
        self.button_create.clicked.connect(self.create_inputs)
        self.layout.addWidget(self.button_create)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.button_calculate = QPushButton("计算均分")
        self.button_calculate.clicked.connect(self.calculate_weighted_average)

        self.button_close = QPushButton("关闭")
        self.button_close.clicked.connect(self.close)

        self.setLayout(self.layout)

    def create_inputs(self):
        rows = int(self.row_input.text())
        self.inputs = []
        self.course = []
        self.weights = []
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(QLabel("科目"), 0, 0)
        self.grid_layout.addWidget(QLabel("成绩"), 0, 1)
        self.grid_layout.addWidget(QLabel("学分"), 0, 2)
        for row in range(1, rows + 1):
            input_course = QLineEdit()
            self.grid_layout.addWidget(input_course, row, 0)
            self.course.append(input_course)

            input_array = QLineEdit()
            self.grid_layout.addWidget(input_array, row, 1)
            self.inputs.append(input_array)

            input_weight = QLineEdit()
            self.grid_layout.addWidget(input_weight, row, 2)
            self.weights.append(input_weight)

        self.layout.addLayout(self.grid_layout)
        self.layout.addWidget(self.button_close)
        self.layout.addWidget(self.button_calculate)

    def calculate_weighted_average(self):
        total_weight = 0
        weighted_sum = 0
        for i, input_array in enumerate(self.inputs):
            try:
                value = float(input_array.text())
                weight = float(self.weights[i].text())
                total_weight += weight
                weighted_sum += value * weight
            except ValueError:
                pass

        if total_weight != 0:
            average = weighted_sum / total_weight
            self.result_label.setText(f"均分：{average}")
        else:
            self.result_label.setText("无法计算均分")
        font = QFont()
        font.setPointSize(30)
        self.result_label.setFont(font)
        self.save_detail()

    def save_detail(self):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(file="./log.txt", mode="a+", encoding="UTF-8") as f:
            f.write("******************************************************************" + "\n")
            f.write(str(current_time) + "\n")
            for i, input_array in enumerate(self.inputs):
                try:
                    f.write(f"科目："
                            + str(self.course[i].text())
                            + f" ,成绩："
                            + str(input_array.text())
                            + f" ,学分："
                            + str(self.weights[i].text())
                            + "\n")
                except ValueError:
                    pass
            f.write(str(self.result_label.text()) + "\n")
            f.write("******************************************************************" + "\n")
            f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon("./icon.ico"))
    window.show()
    sys.exit(app.exec_())
