# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作
# Tkinter:
# Tkinter是Python标准库中自带的GUI库，因此不需要额外安装。
# 它提供了相对简单的接口，适合初学者。然而，它的外观相对较为简单，可能不如其他库提供的现代化外观。
# Tkinter基于Tk GUI工具包，它是一个跨平台的工具包，但在某些平台上可能没有其他库那么好看。
#
# PyQt:
# PyQt是基于Qt库的Python绑定，Qt是一个强大且成熟的C++ GUI库。
# PyQt提供了丰富的功能和现代化的外观，支持大量的组件和特性。
# PyQt是一个相对重量级的库，但也因此提供了更多的灵活性和功能。
#
# wxPython:
# wxPython是基于wxWidgets库的Python绑定，wxWidgets是一个用C++编写的跨平台GUI库。
# wxPython提供了良好的跨平台性能，并具有相对现代化的外观。
# 它是一个中等规模的库，介于Tkinter和PyQt之间，提供了足够的功能，同时也保持了一定的简单性。

import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, messagebox
import requests
from bs4 import BeautifulSoup

class YourApplication:  # 模組化
    def __init__(self, master):
        self.master = master
        self.master.title("教授亂碼抓取器")

        # 寬度和高度
        self.master.geometry("450x500") 

        # 創建視窗元件pyinstaller --onefile main.py
        self.url_label = Label(master, text="亂碼網址：")
        self.url_label.pack()

        self.url_entry = Entry(master, width=40)
        self.url_entry.pack()

        self.fetch_button = Button(master, text="抓取亂碼", command=self.fetch_chaotic_code)
        self.fetch_button.pack()

        # 創建一個 Frame 來包裝 Text 和 Scrollbar
        self.result_frame = tk.Frame(master)
        self.result_frame.pack(fill="both", expand=True)

        # Text
        self.result_text = Text(self.result_frame, wrap="word", height=5, width=50)
        self.result_text.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = Scrollbar(self.result_frame, command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Label顯示抓取的H1標籤內容
        self.h1_label = Label(master, text="")
        self.h1_label.pack()



    def fetch_chaotic_code(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            response.raise_for_status()  # 檢查是否有錯誤的HTTP響應

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # 找到第一個h1標籤
            h1_tag = soup.find('h1')
            # 取得h1標籤的內容，如果存在
            h1_content = h1_tag.text if h1_tag else "未找到 H1 標籤"
            # 更新Label的內容
            self.h1_label.config(text=f"H1標籤內容：{h1_content}")

            chaotic_code = response.text
            self.result_text.delete(1.0, "end")
            self.result_text.insert("end", chaotic_code)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("錯誤", f"無法獲取亂碼：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YourApplication(root)
    root.mainloop()
