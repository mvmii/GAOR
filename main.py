# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Chrome 並加載當前網址)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import tkinter as tk
from tkinter import Button
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

query = "銘傳大學資訊管理學系"
search_url = f"https://www.google.com/search?q={query}"

# 使用Selenium開啟Edge瀏覽器
driver = webdriver.Edge()  # 請確保已下載並設定好Edge WebDriver的路徑

class YourApplication:  # 模組化
    def __init__(self, master):
        self.master = master
        self.master.title("Google 搜尋")

        # 寬度和高度
        self.master.geometry("350x100")

        self.fetch_button = Button(master, text="查詢", command=self.query_google)
        self.fetch_button.pack(pady=10)

    def query_google(self):
        driver.get(search_url)

        # 等待搜尋結果出現
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc"))
            WebDriverWait(driver, 10).until(element_present)
        except Exception as e:
            print(f"等待搜尋結果出現時發生錯誤: {e}")

        # 找到搜尋結果的第一個連結並點擊
        try:
            first_result = driver.find_element(By.CSS_SELECTOR, "div.tF2Cxc a")
            first_result.click()
        except Exception as e:
            print(f"無法點擊第一個搜尋結果: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YourApplication(root)
    root.mainloop()