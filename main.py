# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install PyQt5

# 簡單說明 GUI類型  目前先使用【PyQt】來實作

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt  # 需要导入 Qt 模块

# 创建应用程序对象
app = QApplication([])

# 创建主窗口
window = QWidget()
window.setWindowTitle("我的GUI專案")
window.setGeometry(100, 100, 400, 500)  # 设置窗口大小为400x500

# 创建垂直布局
layout = QVBoxLayout()

# 创建标签
label = QLabel("歡迎使用我的GUI專案")
label.setAlignment(Qt.AlignCenter)
label.setStyleSheet("background-color: blue; color: white;")  # 设置背景色为蓝色，文字颜色为白色
label.setFixedHeight(100)  # 设置标签的高度为100
layout.addWidget(label)

# 创建按钮
button = QPushButton("點擊我")
layout.addWidget(button)

# 定义一个函数，当按钮被点击时执行
def button_click():
    label.setText("按鈕被點擊了！")

button.clicked.connect(button_click)

# 设置布局
window.setLayout(layout)

# 设置标签和按钮置顶
label.setContentsMargins(10, 10, 10, 10)
button.setContentsMargins(10, 10, 10, 10)

# 显示窗口
window.show()

# 运行应用程序
app.exec_()