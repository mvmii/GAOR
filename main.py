# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Chrome 並加載當前網址)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 使用Selenium開啟Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 在後台執行
driver = webdriver.Chrome(options=chrome_options)

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
            # 加載URL
            driver.get(url)
            # 取得當前網頁HTML
            response_text = driver.page_source

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response_text, 'html.parser')

            # 找到第一個h1標籤
            h1_tag = soup.find('h1')
            # 取得h1標籤的內容，如果存在
            h1_content = h1_tag.text if h1_tag else "未找到 H1 標籤"
            # 更新Label的內容
            self.h1_label.config(text=f"H1標籤內容：{h1_content}")

            # 顯示亂碼在Text中
            self.result_text.delete(1.0, "end")
            self.result_text.insert("end", response_text)

            # 關閉Chrome
            # driver.quit()
            # 關閉當前瀏覽器窗口
            # driver.close()

        except Exception as e:
            messagebox.showerror("錯誤", f"無法獲取亂碼：{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YourApplication(root)
    root.mainloop()
