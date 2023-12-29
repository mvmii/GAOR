# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Edge 並加載當前網址)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import os
import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, StringVar
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 使用Selenium開啟Edge瀏覽器
driver = webdriver.Edge()  # 請確保已下載並設定好Edge WebDriver的路徑

messageLog = ""


class MainApplication:  # 模組化
    def __init__(self, master):
        self.messageLog = ""
        self.master = master
        self.master.title("測試登入")
        # 寬度和高度
        self.master.geometry("450x500")

        # 網址
        self.url_frame = tk.Frame(master)
        self.url_frame.pack()
        # 輸入網址 Str
        self.url_label = Label(self.url_frame, text="輸入網址：")
        self.url_label.pack(side="left")
        # 輸入網址 input
        self.url_entry = Entry(self.url_frame, width=40)
        self.url_entry.pack(side="right")
        self.url_entry.insert(0, "https://www.goopi.co/users/sign_in")

        # 帳號
        self.inputAcc_frame = tk.Frame(master)
        self.inputAcc_frame.pack()
        # 輸入帳號 Str
        self.acc_label = Label(self.inputAcc_frame, text="帳號：")
        self.acc_label.pack(side="left")
        # 輸入帳號 input
        self.acc_entry = Entry(self.inputAcc_frame, width=40)
        self.acc_entry.pack(side="right")
        self.acc_entry.insert(0, "love_8462564@yahoo.com.tw")

        # 密碼
        self.inputSec_frame = tk.Frame(master)
        self.inputSec_frame.pack()
        # 輸入密碼 Str
        self.sec_label = Label(self.inputSec_frame, text="密碼：")
        self.sec_label.pack(side="left")
        # 輸入密碼 input
        # self.sec_entry = Entry(self.inputSec_frame, width=40)  # show="*" 用于隐藏输入的密码
        self.sec_entry = Entry(self.inputSec_frame, width=40)
        self.sec_entry.pack(side="right")
        self.sec_entry.insert(0, "mvmii1234")

        self.fetch_button = Button(master, text="開始", command=self.url_start)
        self.fetch_button.pack(pady=10)

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

    def url_start(self):
        # 登入
        self.login()
        # 確認登入後，取product-item裡的product-id值，並顯示在self.result_text上
        self.fetch_product_ids()

    def fetch_product_ids(self):
        try:
            file_path = 'product_ids.txt'
            web_product_ids = []

            # 等待页面至少有一个 product-item 元素加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'product-item'))
                # EC.presence_of_all_elements_located((By.TAG_NAME, 'product-item'))
            )

            # 找到所有的 product-item 元素
            product_items = driver.find_elements(By.TAG_NAME, 'product-item')

            # 获取前五个 product-item 的 product-id 属性值
            for item in product_items[:5]:
                product_id = item.get_attribute('product-id')
                if product_id:  # 确保 product_id 不是 None
                    web_product_ids.append(product_id)

            # 如果文件不存在，保存网页上的product IDs到文件
            if not os.path.exists(file_path):
                self.add_log("web_ID"+'\n')
                with open(file_path, 'w') as file:
                    for pid in web_product_ids:
                        self.add_log(pid + '\n')
                        file.write(pid + '\n')
                self.add_log("网页上的前五个产品ID已保存到文件。")
            else:
                # 读取文件中的product IDs
                with open(file_path, 'r') as file:
                    file_product_ids = file.read().strip().split('\n')
                self.add_log("file_ID"+'\n')
                for pid in file_product_ids:
                    self.add_log(pid+'\n')

                # 比较网页和文件中的product IDs
                if web_product_ids == file_product_ids:
                    self.add_log("网页上的产品ID与文件中的相同。")
                else:
                    self.add_log("网页上的产品ID与文件中的不同。")
                    # 如果需要更新文件内容，取消注释以下代码
                    # with open(file_path, 'w') as file:
                    #     for pid in web_product_ids:
                    #         file.write(pid + '\n')
                    # self.add_log("文件已更新。")

            # 将网页上的product IDs显示到日志
            # product_ids_text = "\n".join(web_product_ids)
            # self.add_log(product_ids_text)

        except TimeoutException:
            self.add_log("操作超时，商品信息无法交互")
        except Exception as e:
            self.add_log(f"无法获取商品信息：{e}")

    def login(self):
        url = self.url_entry.get()
        acc = self.acc_entry.get()
        sec = self.sec_entry.get()
        try:
            # 加載URL
            driver.get(url)

            # 帳號輸入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, 'mobile_phone_or_email'))
            )
            # 找到帳號輸入框並輸入帳號
            acc_input = driver.find_element(By.NAME, 'mobile_phone_or_email')
            acc_input.clear()
            acc_input.send_keys(acc)

            # 密码输入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-e2e-id='login-password_input']"))
            )
            # 找到密码输入框并输入密码
            sec_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e-id='login-password_input']")
            sec_input.clear()
            sec_input.send_keys(sec)

            # 登入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-e2e-id='login-submit_button']"))
            )
            # 找到登入按鈕並點擊
            login_button = driver.find_element(By.CSS_SELECTOR, "button[data-e2e-id='login-submit_button']")
            login_button.click()
            self.add_log("登入成功!")
        except TimeoutException:
            self.add_log("登入失敗 : 操作超時，元素無法交互")
        except Exception as e:
            self.add_log(f"登入失敗 : 無法獲取亂碼：{e}")

    def add_log(self, msg):
        self.messageLog += (msg + "\n")
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", self.messageLog)
        print(self.messageLog)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
