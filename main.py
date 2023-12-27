# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install PyQt5
#             pyuic5 -x example.ui -o example_ui.py
#             (設計一個ui並轉成py，COOL東西)

# 簡單說明 GUI類型  目前先使用【PyQt】來實作

from PyQt5 import QtWidgets, uic
import sys

# 导入通过 pyuic5 生成的 Python 文件
from example_ui import Ui_Dialog  # 注意這裡的類名應該是 Ui_Dialog

class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(MyDialog, self).__init__()

        # 使用 loadUiType 加载 .ui 文件
        uic.loadUiType('example.ui', self)

        # 设置 UI
        self.setupUi(self)

        # 在這裡添加其他初始化代碼

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.exec_()
    sys.exit(app.exec_())