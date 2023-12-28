# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Chrome 並加載當前網址)
#             pip install webdriver_manager  (動態下載和管理Chromedriver)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import tkinter as tk
from tkinter import Button, Label
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # 引入 ChromeDriverManager
import os
import subprocess
import logging

query = "銘傳大學資訊管理學系"
search_url = f"https://www.google.com/search?q={query}"

class YourApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Google 搜尋")
        self.master.geometry("350x100")

        # 設定 webdriver_manager 的日誌級別為 WARNING
        logging.getLogger('webdriver_manager').setLevel(logging.WARNING)

        self.fetch_button = Button(master, text="查詢", command=self.query_google)
        self.fetch_button.pack(pady=10)

        self.error_label = Label(master, text="", fg="red")
        self.error_label.pack()

        self.driver = None

        chrome_version = self.get_chrome_version()
        if chrome_version:
            self.fetch_button.config(state=tk.NORMAL)
            self.error_label.config(text="")
            print(f"Detected Chrome version: {chrome_version}")

            # 使用 ChromeDriverManager 動態下載和管理 Chromedriver
            # chromedriver_path = ChromeDriverManager().install()

            # 創建 ChromeOptions
            chrome_options = webdriver.ChromeOptions()

            # 單獨指定 chrome 可執行文件的路徑
            chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

            # 初始化 webdriver.Chrome，傳遞 options 參數
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.fetch_button.config(state=tk.DISABLED)
            self.error_label.config(text="無法獲取Chrome瀏覽器版本")
            print("無法獲取Chrome瀏覽器版本")

    def query_google(self):
        if not self.driver:
            print("未初始化驅動程序")
            return

        self.driver.get(search_url)

        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc"))
            WebDriverWait(self.driver, 10).until(element_present)
        except Exception as e:
            print(f"等待搜尋結果出現時發生錯誤: {e}")

        try:
            first_result = self.driver.find_element(By.CSS_SELECTOR, "div.tF2Cxc a")
            first_result.click()
        except Exception as e:
            print(f"無法點擊第一個搜尋結果: {e}")

    def get_chrome_version(self):
        try:
            # 直接指定 Chrome 可執行文件的路徑
            chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 修改為你的實際路徑

            if os.path.exists(chrome_path):
                # 使用找到的可執行文件路徑獲取版本
                result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True)
                version_str = result.stdout.strip()
                version = version_str.split()[-1]
                return version
            else:
                print("找不到 Chrome 可執行文件")
                return None
        except Exception as e:
            print(f"無法獲取 Chrome 瀏覽器版本: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = YourApplication(root)
    root.mainloop()